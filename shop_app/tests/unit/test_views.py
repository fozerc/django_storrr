from django.test import TestCase, RequestFactory
from django.forms import Form
from shop_app.constants import PRODUCT_PRICE_TEST, PRODUCT_AMOUNT_TEST
from shop_app.forms import PurchaseForm, ReturnForm
from shop_app.models import Product, ShopUser, Purchase, Return
from shop_app.views import PurchaseCreateView, ReturnCreateView, ReturnApproveDeleteView


class PurchaseViewTestCase(TestCase):
    def test_get_form_kwargs(self):
        request = RequestFactory().get('/')
        view = PurchaseCreateView()
        view.setup(request)
        context = view.get_form_kwargs()
        self.assertIn('request', context)

    def test_form_valid(self):
        user = ShopUser.objects.create_user(username='test', password='parol')
        product = Product.objects.create(name='test', price=PRODUCT_PRICE_TEST, amount=PRODUCT_AMOUNT_TEST)
        request = RequestFactory().post('/')
        request.user = user
        data = {'product_id': str(product.pk), 'quantity': 5}
        pf = PurchaseForm(data, request=request)
        pf.is_valid()
        view = PurchaseCreateView()
        view.setup(request)
        response = view.form_valid(form=pf)
        self.assertEqual(response.status_code, 302)
        purchase = view.object
        self.assertIsInstance(purchase, Purchase)
        self.assertEqual(purchase.quantity, 5)
        self.assertEqual(purchase.product.amount, 95)
        self.assertEqual(purchase.user.user_wallet, 9950)


class ReturnViewTestCase(TestCase):
    def test_get_form_kwargs(self):
        request = RequestFactory().get('/')
        view = ReturnCreateView()
        view.setup(request)
        context = view.get_form_kwargs()
        self.assertIn('request', context)


# class ReturnApproveDeleteViewTestCase(TestCase):
#     def test_form_valid(self):
#         user = ShopUser.objects.create_user(username='test', password='parol')
#         product = Product.objects.create(name='test', price=PRODUCT_PRICE_TEST, amount=PRODUCT_AMOUNT_TEST)
#         purchase = Purchase.objects.create(user=user, product=product, quantity=5)
#         ret = Return.objects.create(purchase=purchase)
#         request = RequestFactory().post('/')
#         form = Form()
#         form.is_valid()
#         view = ReturnApproveDeleteView()
#         view.setup(request)
#         context = view.form_valid(form=form)
