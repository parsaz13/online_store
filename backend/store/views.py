from django.shortcuts import render
from rest_framework import viewsets
from .models import User, Address, Category, Product, ProductImage, Store, StoreItem, Cart, CartItem, Order, OrderItem, Payment, Discount, Comment
from .serializers import UserSerializer, AddressSerializer, CategorySerializer, ProductSerializer, ProductImageSerializer, StoreSerializer, StoreItemSerializer, CartSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer, PaymentSerializer, DiscountSerializer, CommentSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils.translation import gettext as _
import redis
import random
from django.conf import settings
from django.core.mail import send_mail
from store.models import User
from rest_framework import status
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
import random
from celery import shared_task

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

class StoreItemViewSet(viewsets.ModelViewSet):
    queryset = StoreItem.objects.all()
    serializer_class = StoreItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    # Registration logic (simplified)
    data = request.data
    if User.objects.filter(email=data.get('email')).exists():
        return Response({'detail': _('Email already exists.')}, status=400)
    user = User.objects.create(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        username=data.get('username'),
        phone=data.get('phone'),
        password=data.get('password'),
        role='customer',
    )
    return Response({'detail': _('Registration successful.')}, status=201)

@api_view(['POST'])
@permission_classes([AllowAny])
def otp_request(request):
    email = request.data.get('email')
    if not User.objects.filter(email=email).exists():
        return Response({'detail': _('User not found.')}, status=404)
    otp = random.randint(100000, 999999)
    cache.set(f'otp_{email}', otp, timeout=300)
    send_otp_email.delay(email, otp)
    return Response({'detail': _('OTP sent.')})

@api_view(['POST'])
@permission_classes([AllowAny])
def otp_login(request):
    email = request.data.get('email')
    otp = request.data.get('otp')
    cached_otp = cache.get(f'otp_{email}')
    if str(otp) == str(cached_otp):
        user = User.objects.get(email=email)
        # Issue JWT token (pseudo, should use SimpleJWT)
        return Response({'detail': _('Login successful.'), 'token': 'jwt_token_here'})
    return Response({'detail': _('Invalid OTP.')}, status=400)

@shared_task
def send_otp_email(email, otp):
    send_mail(
        _('Your OTP Code'),
        _('Your OTP code is: ') + str(otp),
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
