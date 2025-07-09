from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, AddressViewSet, CategoryViewSet, ProductViewSet, ProductImageViewSet, StoreViewSet, StoreItemViewSet, CartViewSet, CartItemViewSet, OrderViewSet, OrderItemViewSet, PaymentViewSet, DiscountViewSet, CommentViewSet, register, otp_request, otp_login
)
from django.urls import path

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-images', ProductImageViewSet)
router.register(r'stores', StoreViewSet)
router.register(r'store-items', StoreItemViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'discounts', DiscountViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = router.urls 
urlpatterns += [
    path('auth/register/', register, name='register'),
    path('auth/otp/request/', otp_request, name='otp_request'),
    path('auth/otp/login/', otp_login, name='otp_login'),
] 