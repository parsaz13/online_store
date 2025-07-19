from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import CustomUser


class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        self.email = "zarchiniparsa68@gmail.com"
        self.password = "1234papa"
        self.username = "parsaz001"
        self.first_name = "Parsa"
        self.last_name = "Zarchini"

        self.user = CustomUser.objects.create_user(
            email=self.email,
            password=self.password,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
        )

    def test_user_registration(self):
        url = reverse('register')
        data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "first_name": "Ali",
            "last_name": "Ahmadi",
            "password": "testpass123",
            "password2": "testpass123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email="newuser@example.com").exists())

    def test_send_otp(self):
        url = reverse('get_otp')
        data = {
            "email": self.email,
            "password": self.password
        }
        response = self.client.post(url, data, format='json')
        print("OTP SEND:", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_verify_otp(self):
        otp = 123456
        cache.set(f"login_otp_{self.email}", otp, timeout=300)
        url = reverse('verify_otp')
        data = {
            "email": self.email,
            "otp": otp
        }
        response = self.client.post(url, data, format='json')
        print("OTP VERIFY:", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
