from django.contrib import admin

from shop_app.models import Product, ProductForPurchase, Return

admin.site.register(Product)
admin.site.register(ProductForPurchase)
admin.site.register(Return)
