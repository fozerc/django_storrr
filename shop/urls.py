"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

from shop_app.cart.cart import Cart
from shop_app.views import RegisterView, ProductListView, PurchaseCreateView, ProfileListView, ReturnCreateView, \
    ReturnApproveDeleteView, ReturnDeclineDeleteView, ProductCreateView, ReturnListView, AddToCartView, CartListView, \
    RemoveFromCartView, PurchaseFromCartCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', ProductListView.as_view(), name='index'),
    path('purchase/', PurchaseCreateView.as_view(), name='purchase'),
    path('profile/', ProfileListView.as_view(), name='profile'),
    path('create-return/', ReturnCreateView.as_view(), name='create_return'),
    path('return-approve/<int:pk>/', ReturnApproveDeleteView.as_view(), name='return_approve'),
    path('return-decline/<int:pk>/', ReturnDeclineDeleteView.as_view(), name='return_decline'),
    path('product_create/', ProductCreateView.as_view(), name='create_product'),
    path('return-list/', ReturnListView.as_view(), name='returns_list'),
    path('add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CartListView.as_view(), name='cart_list'),
    path('delete-from-cart/<int:product_id>', RemoveFromCartView.as_view(), name='delete_from_cart'),
    path('purchase-cart/',  PurchaseFromCartCreateView.as_view(), name='buy_from_cart'),
    path('api/', include('shop_app.api.urls'))
              ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


