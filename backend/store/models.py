from django.db import models
from products.models import Product
from django.conf import settings

class Store(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    owner  = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    description = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.owner}"

class StoreItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) 
    quantity = models.IntegerField()
    is_listed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product} - {self.store}"

    @property
    def final_price(self):
        if self.discount_percentage:
            return self.price * (1 - self.discount_percentage / 100)
        return self.price