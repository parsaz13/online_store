from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Product, Category
from store.models import Store, StoreItem
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class ProductViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="seller@example.com",
            username="seller1",
            password="test123",
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
        self.storeitem = StoreItem.objects.create(
            product=self.product,
            store=self.store,
            price=1500.00,
            discount_percentage=10.00,
            quantity=10,
            is_listed=True
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

    def test_top_selling_products(self):
        self.storeitem.sales_count = 5
        self.storeitem.save()
        url = reverse('top-selling')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Gaming Laptop")
        self.assertEqual(response.data[0]['store_items'][0]['sales_count'], 5)