from rest_framework import viewsets, filters, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from products.models import Product, Category, ProductImage
from store.models import StoreItem
from django.db.models import Subquery, OuterRef
from .serializers import ProductSerializer, CategorySerializer, ProductImageSerializer
from store.permissions import IsStoreOwner
from django.db.models import Q, Sum

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
    queryset = self.queryset.prefetch_related('images', 'storeitem_set__store').distinct()
    min_price = self.request.query_params.get('min_price')
    max_price = self.request.query_params.get('max_price')
    brand = self.request.query_params.get('brand')
    ordering = self.request.query_params.get('ordering')
    category_slug = self.request.query_params.get('category_slug')

    if category_slug:
        queryset = queryset.filter(category__slug=category_slug)
    if min_price:
        queryset = queryset.filter(storeitem__final_price__gte=min_price)
    if max_price:
        queryset = queryset.filter(storeitem__final_price__lte=max_price)
    if brand:
        queryset = queryset.filter(brand__iexact=brand)
    if ordering == '-storeitem__sales_count':
        queryset = queryset.annotate(total_sales=Sum('storeitem__sales_count')).order_by('-total_sales')
    return queryset

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
                'description': category.get('description', ''),
                'children': []
            }
            children = queryset.filter(parent_id=category['id'])
            for child in children:
                child_data = self.get_serializer(child).data
                node['children'].append(build_tree(child_data))
            return node

        tree = [build_tree(category) for category in serializer.data]
        return Response(tree)

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.filter(is_deleted=False)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsStoreOwner]

class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.filter(is_deleted=False)
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsStoreOwner]

    def perform_create(self, serializer):
        serializer.save()

class TopSellingProductsView(generics.ListAPIView):
    queryset = Product.objects.filter(is_deleted=False, storeitem__sales_count__gt=0)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return self.queryset.prefetch_related('images', 'storeitem_set__store').annotate(
            total_sales=Sum('storeitem__sales_count')
        ).order_by('-total_sales').distinct()[:10]


class SalesChartView(generics.ListAPIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(is_deleted=False).annotate(
            total_sales=Subquery(
                StoreItem.objects.filter(product=OuterRef('pk')).values('product').annotate(
                    total_sales=Sum('sales_count')
                ).values('total_sales')[:1]
            )
        ).values('title', 'total_sales')
        data = {
            'labels': [p['title'] for p in products],
            'sales': [p['total_sales'] or 0 for p in products]
        }
        return Response(data)

class ProductImageUploadView(generics.CreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated, IsStoreOwner]

    def perform_create(self, serializer):
        product_id = self.kwargs['product_id']
        product = Product.objects.get(id=product_id)
        serializer.save(product=product)