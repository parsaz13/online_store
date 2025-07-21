from rest_framework import serializers
from .models import Store, StoreItem

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["id", "name", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at"]


class StoreItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreItem
        fields = '__all__'
        read_only_fields = ['id', 'final_price']
