from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser
from store.models import Store, StoreItem
from products.models import Product, Category
from rest_framework_simplejwt.tokens import RefreshToken

class StoreItemCreateTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="seller@example.com",
            username="seller1",
            password="test123",
            first_name="Seller",
            last_name="One",
            phone="09123456789",
            role="store_owner"
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
        self.store = Store.objects.create(
            name="My Store",
            slug="my-store",
            owner=self.user,
            description="A great store"
        )
        self.item_data = {
            "product": self.product.id,
            "price": 1500.00,
            "discount_percentage": 10.00,
            "quantity": 10,
            "is_listed": True
        }

    def test_create_store_item(self):
        store = Store.objects.create(
            name="Test Store",
            slug="test-store",
            owner=self.user,
            description="Test store description"
        )
        url = reverse('store-item-create')
        response = self.client.post(url, self.item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(StoreItem.objects.count(), 1)
        self.assertEqual(StoreItem.objects.first().quantity, 10)
        self.assertEqual(StoreItem.objects.first().final_price, 1350.00)

    def test_create_store_item_without_store(self):
        self.store.delete()
        url = reverse('store-item-create')
        response = self.client.post(url, self.item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("store", str(response.data))