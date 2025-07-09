from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Product, Cart, Order

# Create your tests here.

class UserModelTest(APITestCase):
    def test_create_user(self):
        user = User.objects.create(
            first_name='Ali', last_name='Test', email='ali@test.com', username='ali', phone='09120000000', password='pass', role='customer')
        self.assertEqual(user.email, 'ali@test.com')

class ProductModelTest(APITestCase):
    def test_create_product(self):
        user = User.objects.create(first_name='Ali', last_name='Test', email='ali2@test.com', username='ali2', phone='09120000001', password='pass', role='customer')
        product = Product.objects.create(title='Test Product', slug='test-product', brand='Brand', description='desc', status=True, category_id_id=1)
        self.assertEqual(product.title, 'Test Product')

class UserAPITest(APITestCase):
    def test_register(self):
        url = reverse('register')
        data = {'first_name': 'Ali', 'last_name': 'Test', 'email': 'ali3@test.com', 'username': 'ali3', 'phone': '09120000002', 'password': 'pass'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ProductAPITest(APITestCase):
    def test_list_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
