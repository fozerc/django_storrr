from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from shop_app.api.permissions import IsAdminOrReadOnly, IsAdminReturnActions
from shop_app.api.serializers import RegisterSerializer, ProductSerializer, PurchaseSerializer, ReturnSerializer
from shop_app.models import ShopUser, Product, ProductForPurchase, Return


class RegisterApiView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []
    queryset = ShopUser.objects.all()


class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post', 'patch']


class PurchaseModelViewSet(viewsets.ModelViewSet):
    queryset = ProductForPurchase.objects.all()
    serializer_class = PurchaseSerializer
    http_method_names = ['get', 'post']

    def get_queryset(self):
        return ProductForPurchase.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        user = self.request.user
        quantity = serializer.validated_data['quantity']
        product.amount -= quantity
        user.user_wallet -= product.price * quantity
        with transaction.atomic():
            product.save()
            user.save()
            serializer.save(user=self.request.user)


class ReturnModelViewSet(viewsets.ModelViewSet):
    queryset = Return.objects.all()
    permission_classes = [IsAdminReturnActions]
    serializer_class = ReturnSerializer
    http_method_names = ['get', 'post']

    def get_queryset(self):
        query = Q()
        if not self.request.user.is_superuser:
            query |= Q(purchase__user=self.request.user)
        return Return.objects.filter(query)

    @action(methods=['post'], detail=True)
    def approve(self, request, pk=None):
        ret = self.get_object()
        purchase = ret.purchase
        product = purchase.product
        quantity = purchase.quantity
        user = purchase.user
        price = product.price
        user.user_wallet += quantity * price
        product.amount += quantity
        with transaction.atomic():
            product.save()
            user.save()
            purchase.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True)
    def decline(self, request, pk=None):
        ret = self.get_object()
        ret.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
