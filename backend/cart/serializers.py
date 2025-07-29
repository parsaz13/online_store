from rest_framework import serializers
from .models import Cart, CartItem
from store.serializers import StoreItemSerializer
from store.models import StoreItem

class CartItemSerializer(serializers.ModelSerializer):
    storeitem = StoreItemSerializer(read_only=True)
    storeitem_id = serializers.IntegerField(write_only=True, source='storeitem.id')

    class Meta:
        model = CartItem
        fields = ['id', 'storeitem', 'storeitem_id', 'quantity', 'price_at_time', 'created_at', 'updated_at']
        read_only_fields = ['id', 'price_at_time', 'created_at', 'updated_at']

    def validate(self, data):
        storeitem_id = data.get('storeitem').get('id')
        quantity = data.get('quantity')
        try:
            storeitem = StoreItem.objects.get(id=storeitem_id, is_deleted=False, is_listed=True)
            if storeitem.quantity < quantity:
                raise serializers.ValidationError(f"Only {storeitem.quantity} items available in stock.")
        except StoreItem.DoesNotExist:
            raise serializers.ValidationError("StoreItem does not exist.")
        return data

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'items', 'total_price', 'created_at', 'updated_at']

    def get_total_price(self, obj):
        return sum(item.price_at_time * item.quantity for item in obj.cartitem_set.filter(is_deleted=False))