from django.db import models

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    class Meta:
        abstract = True

# --- Accounts ---
class User(SoftDeleteModel):
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

class Address(SoftDeleteModel):
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

# --- Catalog ---
class Category(SoftDeleteModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product(SoftDeleteModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    brand = models.CharField(max_length=255)
    description = models.TextField()
    status = models.BooleanField(default=True)
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductImage(models.Model):
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

# --- Storefront ---
class Store(SoftDeleteModel):
    name = models.CharField(max_length=255)
    manager_id = models.ForeignKey('User', on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class StoreItem(SoftDeleteModel):
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    store_id = models.ForeignKey('Store', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    is_listed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# --- Cart ---
class Cart(SoftDeleteModel):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    discount_id = models.ForeignKey('Discount', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(SoftDeleteModel):
    cart_id = models.ForeignKey('Cart', on_delete=models.CASCADE)
    storeitem_id = models.ForeignKey('StoreItem', on_delete=models.CASCADE)
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# --- Order/Checkout ---
class Order(SoftDeleteModel):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    discount_id = models.ForeignKey('Discount', on_delete=models.CASCADE)
    address_id = models.ForeignKey('Address', on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(SoftDeleteModel):
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE)
    storeitem_id = models.ForeignKey('StoreItem', on_delete=models.CASCADE)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Payment(SoftDeleteModel):
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    authority_code = models.CharField(max_length=255)
    transaction_id = models.CharField(max_length=255)
    paid_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# --- Discounts ---
class Discount(SoftDeleteModel):
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

# --- Reviews/Comments ---
class Comment(SoftDeleteModel):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    store_id = models.ForeignKey('Store', on_delete=models.CASCADE)
    comment = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
