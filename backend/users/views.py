# views.py
import random
from .serializers import UserSerializer
from django.core.cache import cache
from django.contrib.auth import authenticate
from django.contrib.auth import login , logout
from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.active()
    serializer_class = RegisterSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": f"Hello, {request.user.username}. You have successfully logged in."})


@api_view(['POST'])
def get_otp(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(email=email, password=password)
    if user is None:
        return Response({"error": "Invalid email or password."}, status=400)
    otp = random.randint(100000, 999999)
    cache.set(f'login_otp_{email}', otp, timeout=300)
    return Response({
        "message": "OTP sent successfully.",
        "otp": otp
    })


@api_view(['POST'])
def verify_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otp')
    if not email or not otp:
        return Response({"error": "Email and OTP are required."}, status=400)

    try:
        otp = int(otp)
    except ValueError:
        return Response({"error": "OTP must be a number."}, status=400)

    real_otp = cache.get(f'login_otp_{email}')
    if real_otp != otp:
        return Response({'error': 'Invalid OTP'}, status=400)

    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)

    login(request, user)

    refresh = RefreshToken.for_user(user)
    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "message": "Login verified successfully."
    })

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    user.delete()
    return Response({'message': 'User deleted logically.'}, status=200)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return Response({"message": "Logged out successfully."}, status=200)
    return Response({"error": "You are not logged in."}, status=400)

