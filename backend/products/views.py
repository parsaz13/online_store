from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from store.serializers import StoreItemSerializer
from store.models import StoreItem

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_deleted=False)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__id', 'storeitem__store__id']
    search_fields = ['title', 'brand', 'description']
    ordering_fields = ['created_at', 'title', 'storeitem__final_price', 'storeitem__sales_count']
    ordering = ['-created_at']

    def get_queryset(self):
        return self.queryset.prefetch_related('images', 'storeitem_set__store')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        store_items = StoreItem.objects.filter(product=instance, is_deleted=False, is_listed=True)
        store_items_data = StoreItemSerializer(store_items, many=True).data
        data = serializer.data
        data['store_items'] = store_items_data
        return Response(data)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_deleted=False)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return self.queryset.select_related('parent')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        root_categories = queryset.filter(parent__isnull=True)
        serializer = self.get_serializer(root_categories, many=True)
        
        def build_tree(category):
            node = {
                'id': category['id'],
                'name': category['name'],
                'slug': category['slug'],
                'description': category['description'],
                'children': []
            }
            children = queryset.filter(parent_id=category['id'])
            for child in children:
                child_data = self.get_serializer(child).data
                node['children'].append(build_tree(child_data))
            return node

        tree = [build_tree(category) for category in serializer.data]
        return Response(tree)