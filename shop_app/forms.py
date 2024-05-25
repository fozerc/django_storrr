from datetime import timedelta

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django import forms
from django.utils.timezone import now

from shop.settings import RETURN_ALLOWED_TIME
from shop_app.models import ShopUser, ProductForPurchase, Product, Return, Purchasing


class RegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username',)


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = ProductForPurchase
        exclude = ('product',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        product = self.check_product_exist()
        quantity = cleaned_data.get('quantity')
        self.check_product_quantity(quantity, product)
        self.check_user_wallet(quantity, product)
        self.product = product
        return cleaned_data

    def check_product_exist(self):
        product_id = self.data.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            messages.error(self.request, 'Product does not exist')
            raise forms.ValidationError('Product does not exist')
        return product

    def check_product_quantity(self, quantity, product):
        if quantity > product.quantity:
            messages.error(self.request, 'Not enough quantity available')
            self.add_error(None, 'Not enough quantity available')

    def check_user_wallet(self, quantity, product):
        if quantity * product.quantity > self.request.user.user_wallet:
            messages.error(self.request, 'You have not enough money')
            self.add_error(None, 'You have not enough money')


class PurchaseFromCartForm(forms.ModelForm):
    class Meta:
        model = Purchasing
        exclude = ('products',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        cart = self.request.cart.cart
        products = self.check_products_exist(cart)
        quantities = list(cart.values())
        self.check_products_quantity(products, quantities)
        self.products_price = self.check_user_wallet(products, quantities)
        self.products = products
        self.quantities = quantities

    def check_products_exist(self, cart):
        products = []
        for product_id in cart:
            try:
                product = Product.objects.get(pk=product_id)
                products.append(product)
            except Product.DoesNotExist:
                messages.error(self.request, "You're trying to buy a non-existent product")
                raise forms.ValidationError("You're trying to buy a non-existent product")
        return products

    def check_products_quantity(self, products, quantities):
        for product, quantity in zip(products, quantities):
            quantity_int = int(quantity['quantity'])
            if quantity_int > product.quantity:
                messages.error(self.request, 'Not enough quantity available')
                self.add_error(None, 'Not enough quantity available')

    def check_user_wallet(self, products, quantities):
        products_price = []
        for product, quantity in zip(products, quantities):
            quantity_int = int(quantity['quantity'])
            products_price.append(product.price * quantity_int)
        if sum(products_price) > self.request.user.user_wallet:
            messages.error(self.request, 'You have not enough money')
            self.add_error(None, 'You have not enough money')
        return products_price


class ReturnForm(forms.ModelForm):
    class Meta:
        model = Return
        exclude = ('purchase',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        purchase = self.check_purchase_exist()
        self.check_return_time(purchase)
        self.purchase = purchase
        return cleaned_data

    def check_purchase_exist(self):
        purchase_id = self.data.get('purchase_id')
        try:
            purchase = ProductForPurchase.objects.get(pk=purchase_id)
        except ProductForPurchase.DoesNotExist:
            messages.error(self.request, 'Purchase does not exist')
            raise forms.ValidationError('Purchase does not exist')
        return purchase

    def check_return_time(self, purchase):
        if (now() - purchase.created_at).seconds > RETURN_ALLOWED_TIME:
            messages.error(self.request, "Return time has expired")
            raise forms.ValidationError('Return time has expired')
