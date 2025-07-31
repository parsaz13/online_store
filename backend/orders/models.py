from django.db import models
from django.conf import settings
from users.models import Address
from store.models import StoreItem

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} - {self.user}"

    @property
    def total_price(self):
        return sum(item.price_at_purchase * item.quantity for item in self.orderitem_set.filter(is_deleted=False))

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    storeitem = models.ForeignKey(StoreItem, on_delete=models.CASCADE)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.storeitem.product.title} - Order {self.order.id}"