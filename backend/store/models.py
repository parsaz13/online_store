from django.db import models
from products.models import Product

class Store(models.Model):
    name = models.CharField(max_length=255)
    manager = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE,null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.manager}"

class StoreItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    is_listed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product} - {self.store}"
