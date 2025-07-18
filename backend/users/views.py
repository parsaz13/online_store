import random
from django.shortcuts import render
from django.core.cache import cache
from rest_framework import generics
from .serializers import RegisterSerializer
from .models import CustomUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": f"Hello, {request.user.username}You have successfully logged in."})

@api_view(['POST'])
def send_otp(request):
    phone = request.data.get('phone')
    if not phone:
        return Response({"error": "Phone number is required."}, status=400)
    

    otp = random.randint(100000, 999999)
    
    cache.set(f'otp_{phone}', otp, timeout=300)
    
    return Response({"otp": otp, "message": "OTP sent successfully."})

@api_view(['POST'])
def verify_otp(request):
    phone = request.data.get('phone')
    otp = request.data.get('otp')
    
    if not phone or not otp:
        return Response({"error": "Phone number and OTP are required."}, status=400)

    try:
        otp = int(otp)
    except ValueError:
        return Response({"error": "OTP must be a number."}, status=400)

    real_otp = cache.get(f"otp_{phone}")
    if real_otp != otp:
        return Response({'error': 'Invalid OTP'}, status=400)
    
    user, _ = CustomUser.objects.get_or_create(phone=phone, defaults={
        "email": f"{phone}@otp.com",
        "username": phone,
        "first_name": "NoName",
        "last_name": "User",
    })
    refresh = RefreshToken.for_user(user)
    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "message": "OTP verified successfully."
    })
