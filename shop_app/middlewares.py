from django.utils.deprecation import MiddlewareMixin

from shop_app.cart.cart import Cart


class AddCartMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.cart = Cart(request)
