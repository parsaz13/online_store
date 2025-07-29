from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser
from store.models import Store, StoreItem
from products.models import Product, Category
from .models import Cart, CartItem
from rest_framework_simplejwt.tokens import RefreshToken

class CartViewSetTestCase(APITestCase):
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
        self.cart = Cart.objects.create(user=self.user)

    def test_add_item_to_cart(self):
        url = reverse('cart-add-item')
        data = {
            "storeitem_id": self.storeitem.id,
            "quantity": 2
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.first().quantity, 2)
        self.assertEqual(response.data['total_price'], 2700.00)

    def test_list_cart(self):
        CartItem.objects.create(
            cart=self.cart,
            storeitem=self.storeitem,
            quantity=2,
            price_at_time=self.storeitem.final_price
        )
        url = reverse('cart-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['total_price'], 2700.00)

    def test_update_cart_item(self):
        cart_item = CartItem.objects.create(
            cart=self.cart,
            storeitem=self.storeitem,
            quantity=2,
            price_at_time=self.storeitem.final_price
        )
        url = reverse('cart-update-item', kwargs={'pk': self.cart.id})
        data = {
            "cart_item_id": cart_item.id,
            "quantity": 3
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartItem.objects.first().quantity, 3)
        self.assertEqual(response.data['total_price'], 4050.00)

    def test_remove_cart_item(self):
        cart_item = CartItem.objects.create(
            cart=self.cart,
            storeitem=self.storeitem,
            quantity=2,
            price_at_time=self.storeitem.final_price
        )
        url = reverse('cart-remove-item', kwargs={'pk': self.cart.id})
        data = {
            "cart_item_id": cart_item.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartItem.objects.filter(is_deleted=False).count(), 0)