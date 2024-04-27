from django.test import TestCase

from shop_app.constants import PRODUCT_AMOUNT_TEST, PRODUCT_PRICE_TEST
from shop_app.models import ShopUser, Product


class PurchaseTestCase(TestCase):
    def test_purchase(self):
        user = ShopUser.objects.create_user(username='test', password='parol')
        product = Product.objects.create(name='test', price=PRODUCT_PRICE_TEST, amount=PRODUCT_AMOUNT_TEST)
        self.client.force_login(user)
        data = {'product_id': str(product.pk), 'quantity': 5}
        response = self.client.post("/purchase/", data=data)
        self.assertEqual(response.status_code, 302)
