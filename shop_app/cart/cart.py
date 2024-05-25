class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        self.cart = cart
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add_to_cart(self, product, quantity=1):
        product_id = product.id
        if product_id not in self.cart:
            self.cart[product.id] = {
                'quantity': str(0),
            }

        self.cart[product.id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def remove_from_cart(self, product):
        if str(product.id) in self.cart:
            del self.cart[str(product.id)]
        self.save()
