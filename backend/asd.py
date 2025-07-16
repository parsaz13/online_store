from django.db import models
from users.models import CustomUser
from products.models import Product

class Cart(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    discount_id = models.ForeignKey('Discount', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

class CartItem(models.Model):
    cart_id = models.ForeignKey('Cart', on_delete=models.CASCADE)
    storeitem_id = models.ForeignKey('StoreItem', on_delete=models.CASCADE)
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Cart {self.id} - {self.user_id}"
    
    
    
from django.db import models
from users.models import CustomUser
from products.models import Product

class Order(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    discount_id = models.ForeignKey('Discount', on_delete=models.CASCADE)
    address_id = models.ForeignKey('Address', on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} - {self.user_id}"

class OrderItem(models.Model):
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE)
    storeitem_id = models.ForeignKey('StoreItem', on_delete=models.CASCADE)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.order_id} - {self.storeitem_id}"



from django.db import models
from users.models import CustomUser
from products.models import Product

class Payment(models.Model):
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    authority_code = models.CharField(max_length=255)
    transaction_id = models.CharField(max_length=255)
    paid_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Payment {self.id} - {self.order_id}"

class Discount(models.Model):
    code = models.CharField(max_length=255)
    discount_type = models.CharField(max_length=255)
    value = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    usage_limit = models.IntegerField()
    per_user_limit = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Discount {self.id} - {self.code}"



from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    brand = models.CharField(max_length=255)
    description = models.TextField()
    status = models.BooleanField(default=True)
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.category_id}"

class ProductImage(models.Model):
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    
    def __str__(self):
        return f"{self.product_id} - {self.image}"



from django.db import models

# Create your models here.
class Comment(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    store_id = models.ForeignKey('Store', on_delete=models.CASCADE)
    comment = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment {self.id} - {self.user_id}"

from django.db import models

# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=255)
    manager_id = models.ForeignKey('User', on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.manager_id}"

class StoreItem(models.Model):
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    store_id = models.ForeignKey('Store', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    is_listed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product_id} - {self.store_id}"
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None,**extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


class Address(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    store_id = models.ForeignKey('Store', on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)
    phone = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Address {self.id} - {self.user_id}"
