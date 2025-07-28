from django.urls import path
from .views import ProductCreateView, CategoryCreateView

urlpatterns = [
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
]