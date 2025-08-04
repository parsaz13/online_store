from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet, CategoryViewSet, TopSellingProductsView ,ProductCreateView,CategoryCreateView, SalesChartView , ProductImageUploadView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('top-selling/', TopSellingProductsView.as_view(), name='top-selling'),
    path('sales-chart/', SalesChartView.as_view(), name='sales-chart'),
    path('products/<int:product_id>/images/', ProductImageUploadView.as_view(), name='product-image-upload'),
]