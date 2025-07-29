from rest_framework import serializers
from .models import Payment
from orders.serializers import OrderSerializer

class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    order_id = serializers.IntegerField(write_only=True, source='order.id')

    class Meta:
        model = Payment
        fields = ['id', 'order', 'order_id', 'amount', 'payment_method', 'status', 'authority_code', 'transaction_id', 'paid_at', 'created_at', 'updated_at']
        read_only_fields = ['id', 'amount', 'status', 'authority_code', 'transaction_id', 'paid_at', 'created_at', 'updated_at']

    def validate(self, data):
        order_id = data.get('order').get('id')
        try:
            order = Order.objects.get(id=order_id, user=self.context['request'].user, is_deleted=False)
            if order.status != 'pending':
                raise serializers.ValidationError("Order is not in pending status.")
        except Order.DoesNotExist:
            raise serializers.ValidationError("Invalid or inaccessible order.")
        return data