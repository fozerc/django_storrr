from unittest.mock import patch
from django.test import TestCase, RequestFactory
from django import forms
from shop_app.constants import PRODUCT_PRICE_TEST, PRODUCT_AMOUNT_TEST
from shop_app.forms import PurchaseForm, ReturnForm
from shop_app.models import ShopUser, Product, Purchase, Return


class PurchaseFormTestCase(TestCase):
    def setUp(self):
        self.user = ShopUser.objects.create_user(username='test', password='parol')
        self.product = Product.objects.create(name='test', price=PRODUCT_PRICE_TEST, amount=PRODUCT_AMOUNT_TEST)
        self.request = RequestFactory().get('/')
        self.request.user = self.user
        self.data = {'product_id': str(self.product.pk), 'quantity': 5}

    def test_purchase_form_init_empty_request(self):
        pf = PurchaseForm()
        self.assertIsNone(pf.request)

    def test_purchase_form_init_contains_request(self):
        request = RequestFactory().get('/')
        pf = PurchaseForm(request=request)
        self.assertEquals(pf.request, request)

    def test_clean(self):
        pf = PurchaseForm(self.data, request=self.request)
        pf.is_valid()
        self.assertEquals(pf.clean(), {'quantity': 5})
        self.assertEquals(pf.product, self.product)

    def test_check_product_exist(self):
        data = {'product_id': str(self.product.pk), 'quantity': 5}
        pf = PurchaseForm(self.data, request=self.request)
        self.assertEquals(pf.check_product_exist(), self.product)

    @patch('shop_app.forms.messages')
    def test_check_product_not_exist(self, mock_messages):
        mock_messages.error.return_value = ""
        data = {'quantity': 5}
        pf = PurchaseForm(data, request=self.request)
        with self.assertRaises(forms.ValidationError) as e:
            pf.check_product_exist()

    @patch('shop_app.forms.messages')
    def test_check_product_exist_incorrect_id(self, mock_messages):
        mock_messages.error.return_value = ""
        data = {'product_id': "10000", 'quantity': 5}
        pf = PurchaseForm(data, request=self.request)
        with self.assertRaises(forms.ValidationError) as e:
            pf.check_product_exist()


class ReturnFormTestCase(TestCase):
    def setUp(self):
        self.user = ShopUser.objects.create_user(username='test', password='parol')
        self.product = Product.objects.create(name='test', price=PRODUCT_PRICE_TEST, amount=PRODUCT_AMOUNT_TEST)
        self.purchase = Purchase.objects.create(user=self.user, product=self.product, quantity=5)
        self.request = RequestFactory().post('/')
        self.request.user = self.user

    def test_return_form_init_empty_request(self):
        rf = ReturnForm()
        self.assertIsNone(rf.request)

    def test_return_form_init_contains_request(self):
        request = RequestFactory().get('/')
        rf = ReturnForm(request=request)
        self.assertEquals(rf.request, request)

    def test_clean(self):
        self.data = {'purchase_id': str(self.purchase.pk)}
        rf = ReturnForm(self.data, request=self.request)
        rf.is_valid()
        self.assertEquals(rf.purchase, self.purchase)

    def test_check_purchase_exist(self):
        self.data = {'purchase_id': str(self.purchase.pk)}
        rf = ReturnForm(self.data, request=self.request)
        self.assertEquals(rf.check_purchase_exist(), self.purchase)

    @patch('shop_app.forms.messages')
    def test_check_purchase_exist_incorrect_id(self, mock_messages):
        mock_messages.error.return_value = ""
        self.data = {'purchase_id': "4981243789"}
        rf = ReturnForm(self.data, request=self.request)
        with self.assertRaises(forms.ValidationError) as e:
            rf.check_purchase_exist()

