from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    brand = models.CharField(max_length=255)
    description = models.TextField()
    status = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.category}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    image = models.ImageField(upload_to='product_images/')
    
    def __str__(self):
        return f"{self.product} - {self.image}"


