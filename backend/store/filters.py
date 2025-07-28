from django_filters import rest_framework as filters
from .models import StoreItem

class StoreItemFilter(filters.FilterSet):
    product_name = filters.CharFilter(field_name='product__name', lookup_expr='icontains')

    class Meta:
        model = StoreItem
        fields = {
            'price': ['exact', 'lt', 'gt'],
            'store__name': ['icontains'],
            'is_listed': ['exact'],
        }
