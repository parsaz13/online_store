from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoreViewSet, StoreItemViewSet
router = DefaultRouter()
router.register("stores", StoreViewSet, basename="seller-stores")
router.register("items", StoreItemViewSet, basename="seller-items")

urlpatterns = [
    path("seller/", include(router.urls)),
]
