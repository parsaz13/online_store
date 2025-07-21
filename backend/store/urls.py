from django.urls import path, include
from .views import StoreCreateView , StoreViewSet ,StoreItemCreateView,StoreItemViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', StoreViewSet, basename='store')
router.register(r'items', StoreItemViewSet, basename='store-item')


urlpatterns = [
    path('create/', StoreCreateView.as_view(), name='store-create'),
    path('', include(router.urls)),
    
    
]

