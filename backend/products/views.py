from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from store.permissions import HasStoreOwnerRole

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.filter(is_deleted=False)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, HasStoreOwnerRole]

class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.filter(is_deleted=False)
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, HasStoreOwnerRole]

    def perform_create(self, serializer):
        serializer.save()  