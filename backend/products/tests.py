from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser
from .models import Category, Product
from store.models import Store, StoreItem

class ProductViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="seller@example.com", username="seller1", password="test123", role="store_owner"
        )
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product = Product.objects.create(
            title="Gaming Laptop", slug="gaming-laptop", brand="Dell",
            description="A high-performance gaming laptop", category=self.category
        )
        self.store = Store.objects.create(name="My Store", slug="my-store", owner=self.user)
        self.store_item = StoreItem.objects.create(
            product=self.product, store=self.store, price=1500.00, discount_percentage=10.00,
            quantity=10, is_listed=True
        )

    def test_list_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Gaming Laptop")

    def test_filter_by_category(self):
        url = reverse('product-list') + '?category__id=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_products(self):
        url = reverse('product-list') + '?search=laptop'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_by_sales_count(self):
        url = reverse('product-list') + '?ordering=-storeitem__sales_count'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)