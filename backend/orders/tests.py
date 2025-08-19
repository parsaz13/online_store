from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser, Address
from store.models import Store, StoreItem
from products.models import Product, Category
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch

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
        self.cart = Cart.objects.get_or_create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            storeitem=self.storeitem,
            quantity=2,
            price_at_time=self.storeitem.final_price
        )

    @patch('orders.views.send_order_confirmation_email.delay')
    def test_create_order_from_cart(self, mock_task):
        mock_task.return_value = None

        # Ensure Address exists
        address = Address.objects.create(
            user=self.user,
            street="Test St",
            city="Test City",
            state="Test State",
            postal_code="54321",
            is_default=True
        )

        # Ensure CartItem exists
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(
            cart=cart,
            storeitem=self.storeitem,
            quantity=2,
            price_at_time=self.storeitem.final_price
        )

        url = reverse('order-list')
        data = {
            "address": address.id,
            "cart": cart.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        
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