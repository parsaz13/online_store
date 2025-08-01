from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from users.models import CustomUser, Address
from store.models import Store, StoreItem
from products.models import Product, Category
from orders.models import Order, OrderItem
from .models import Payment
from rest_framework_simplejwt.tokens import RefreshToken

class PaymentViewSetTestCase(APITestCase):
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
        self.order = Order.objects.create(user=self.user, address=self.address, status='pending')
        self.order_item = OrderItem.objects.create(
            order=self.order,
            storeitem=self.storeitem,
            quantity=2,
            price_at_purchase=self.storeitem.final_price
        )

    def test_create_payment(self):
        url = reverse('payment-list')
        data = {"order_id": self.order.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(Payment.objects.first().amount, 2700.00)
        self.assertEqual(Payment.objects.first().status, 'completed')

    def test_create_duplicate_payment(self):
        url = reverse('payment-list')
        data = {"order_id": self.order.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Order already has a completed payment.", str(response.data))
        self.assertEqual(Payment.objects.count(), 1)

    def test_list_payments(self):
        Payment.objects.create(
            order=self.order,
            amount=2700.00,
            payment_method='online',
            status='completed',
            authority_code='550e8400-e29b-41d4-a716-446655440000',
            transaction_id='550e8400-e29b-41d4-a716-446655440001',
            paid_at=timezone.now()
        )
        url = reverse('payment-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_payment(self):
        payment = Payment.objects.create(
            order=self.order,
            amount=2700.00,
            payment_method='online',
            status='completed',
            authority_code='550e8400-e29b-41d4-a716-446655440000',
            transaction_id='550e8400-e29b-41d4-a716-446655440001',
            paid_at=timezone.now()
        )
        url = reverse('payment-detail', kwargs={'pk': payment.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['amount']), 2700.00)