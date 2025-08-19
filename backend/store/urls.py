from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoreViewSet, StoreItemViewSet, StoreItemCreateView

router = DefaultRouter()
router.register("stores", StoreViewSet, basename="seller-stores")
router.register("items", StoreItemViewSet, basename="seller-items")

urlpatterns = [
    path("seller/", include(router.urls)),
    path('store-items/create/', StoreItemCreateView.as_view(), name='store-item-create')
]
