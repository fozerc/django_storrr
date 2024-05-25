from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

from shop.settings import RETURN_ALLOWED_TIME


class ShopUser(AbstractUser):
    user_wallet = models.IntegerField(default=10000)


class Product(models.Model):
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    price = models.PositiveIntegerField()
    picture = models.ImageField(upload_to='pictures', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Name: {self.name}, Price:  {self.price}, Amount: {self.quantity}"


class ProductForPurchase(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Purchasing(models.Model):
    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE)
    products = models.ForeignKey(ProductForPurchase, on_delete=models.CASCADE, related_name='purchase')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def not_returnable(self):
        return (now() - self.created_at).seconds > RETURN_ALLOWED_TIME


class Return(models.Model):
    purchase = models.OneToOneField(ProductForPurchase, on_delete=models.CASCADE, related_name='ret')
