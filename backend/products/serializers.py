from rest_framework import serializers
from .models import Product, Category, ProductImage
from store.models import StoreItem
from store.serializers import StoreItemSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'parent', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'created_at']
        read_only_fields = ['id', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.filter(is_deleted=False))
    images = ProductImageSerializer(many=True, read_only=True)
    store_items = StoreItemSerializer(many=True, read_only=True, source='storeitem_set')

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'brand', 'description', 'category', 'created_at', 'updated_at', 'images', 'store_items']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at', 'images', 'store_items']

    def create(self, validated_data):
        return Product.objects.create(**validated_data)