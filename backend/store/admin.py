from django.contrib import admin
from .models import User, Address, Category, Product, ProductImage, Store, StoreItem, Cart, CartItem, Order, OrderItem, Payment, Discount, Comment

# Register your models here.

admin.site.register(User)
admin.site.register(Address)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Store)
admin.site.register(StoreItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Discount)
admin.site.register(Comment)
