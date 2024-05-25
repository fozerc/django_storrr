from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from shop_app.api.resourses import RegisterApiView, ProductModelViewSet, PurchaseModelViewSet, ReturnModelViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductModelViewSet)
router.register(r'purchases', PurchaseModelViewSet)
router.register(r'returns', ReturnModelViewSet)

urlpatterns = [
    path('token/', obtain_auth_token, name='token'),
    path('register-api/', RegisterApiView.as_view(), name='register-api'),
    path('', include(router.urls))
]