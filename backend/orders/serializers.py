from rest_framework import serializers
from .models import Order, OrderItem
from store.serializers import StoreItemSerializer
from users.models import Address

class OrderItemSerializer(serializers.ModelSerializer):
    storeitem = StoreItemSerializer(read_only=True)
    storeitem_id = serializers.IntegerField(write_only=True, source='storeitem.id')

    class Meta:
        model = OrderItem
        fields = ['id', 'storeitem', 'storeitem_id', 'quantity', 'price_at_purchase', 'created_at', 'updated_at']
        read_only_fields = ['id', 'price_at_purchase', 'created_at', 'updated_at']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    address_id = serializers.IntegerField(write_only=True, source='address.id')
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'address', 'address_id', 'status', 'items', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'items', 'total_price', 'created_at', 'updated_at']

    def get_total_price(self, obj):
        return sum(item.price_at_purchase * item.quantity for item in obj.orderitem_set.filter(is_deleted=False))

    def validate(self, data):
        address_id = data.get('address').get('id')
        try:
            address = Address.objects.get(id=address_id, user=self.context['request'].user, is_deleted=False)
        except Address.DoesNotExist:
            raise serializers.ValidationError("Invalid or inaccessible address.")
        return data