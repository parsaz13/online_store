#urls
from django.urls import path , include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import RegisterView, protected_view, get_otp, verify_otp, UserProfileView, delete_user, logout_view, AddressViewSet


router = DefaultRouter()
router.register(r'addresses', AddressViewSet, basename='address')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('protected/', protected_view, name='protected'),
    path('login/', get_otp, name='get_otp'),
    path('login/verify/', verify_otp, name='verify_otp'),
    path('logout/', logout_view, name='logout'),
    path('delete/', delete_user, name='delete_user'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('', include(router.urls)),
]

