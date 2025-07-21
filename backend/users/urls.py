#urls
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, protected_view  , get_otp, verify_otp, UserProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('protected/', protected_view, name='protected'),
    path('login/', get_otp, name='get_otp'),
    path('login/verify/', verify_otp, name='verify_otp'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]

