from django.core.validators import MinValueValidator
from django.db.models import Q
from rest_framework import serializers
from shop_app.models import ShopUser, Product, Purchase, Return


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = ShopUser
        fields = ['username', 'email', 'password']

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        user_exist = Q(username__iexact=username) | Q(email__iexact=email)
        if ShopUser.objects.filter(user_exist).count():
            raise serializers.ValidationError('This user is already registered.')
        return attrs

    def create(self, validated_data):
        return ShopUser.objects.create_user(**validated_data)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['description', 'amount', 'name', 'price', 'picture', 'id']


class PurchaseSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(required=True, validators=[MinValueValidator(0)])

    class Meta:
        model = Purchase
        fields = ['id', 'product', 'quantity']

    def validate(self, attrs):
        product = attrs.get('product')
        quantity = attrs.get('quantity')
        user = self.context['request'].user
        if product.amount < quantity:
            raise serializers.ValidationError('We have not enough quantity for this product.')
        if user.user_wallet < product.price * quantity:
            raise serializers.ValidationError('You do not have enough money.')
        return attrs


class ReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Return
        fields = ['id', 'purchase']

    def validate(self, attrs):
        purchase = attrs.get('purchase')
        user = self.context['request'].user
        if purchase.user != user:
            raise serializers.ValidationError('You can only return your purchases.')
        if purchase.not_returnable:
            raise serializers.ValidationError('Return time is expired')
        return attrs