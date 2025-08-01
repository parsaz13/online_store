from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser, Address
from store.models import Store, StoreItem
from products.models import Product, Category
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from rest_framework_simplejwt.tokens import RefreshToken

class OrderViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="customer@example.com",
            username="customer1",
            password="test123",
            first_name="Customer",
            last_name="One",
            phone="09123456789",
            role="customer"
        )
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product = Product.objects.create(
            title="Gaming Laptop",
            slug="gaming-laptop",
            brand="Dell",
            description="A high-performance gaming laptop",
            category=self.category
        )
        self.store_owner = CustomUser.objects.create_user(
            email="seller@example.com",
            username="seller1",
            password="test123",
            role="store_owner"
        )
        self.store = Store.objects.create(
            name="My Store",
            slug="my-store",
            owner=self.store_owner,
            description="A great store"
        )
        self.storeitem = StoreItem.objects.create(
            product=self.product,
            store=self.store,
            price=1500.00,
            discount_percentage=10.00,
            quantity=10,
            is_listed=True
        )
        self.address = Address.objects.create(
            user=self.user,
            street="Main St",
            city="Tehran",
            state="Tehran",
            postal_code="12345",
            is_default=True
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            storeitem=self.storeitem,
            quantity=2,
            price_at_time=self.storeitem.final_price
        )

    def test_create_order_from_cart(self):
        url = reverse('order-create-from-cart')
        data = {"address_id": self.address.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(OrderItem.objects.first().quantity, 2)
        self.assertEqual(response.data['total_price'], 2700.00)
        self.assertEqual(StoreItem.objects.first().quantity, 8) 
        self.assertEqual(CartItem.objects.filter(is_deleted=False).count(), 0)

    def test_list_orders(self):
        Order.objects.create(user=self.user, address=self.address, status='pending')
        url = reverse('order-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_order(self):
        order = Order.objects.create(user=self.user, address=self.address, status='pending')
        OrderItem.objects.create(
            order=order,
            storeitem=self.storeitem,
            quantity=2,
            price_at_purchase=self.storeitem.final_price
        )
        url = reverse('order-detail', kwargs={'pk': order.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_price'], 2700.00)