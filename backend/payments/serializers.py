from rest_framework import serializers
from .models import Payment
from orders.models import Order
from orders.serializers import OrderSerializer
from django.utils import timezone
import uuid

class PaymentSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(write_only=True, source='order.id')
    order = OrderSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'order', 'order_id', 'amount', 'payment_method', 'status', 'authority_code', 'transaction_id', 'paid_at', 'created_at', 'updated_at']
        read_only_fields = ['id', 'order', 'amount', 'payment_method', 'status', 'authority_code', 'transaction_id', 'paid_at', 'created_at', 'updated_at']

    def validate(self, data):
        order_id = data.get('order').get('id')
        try:
            order = Order.objects.get(id=order_id, user=self.context['request'].user, is_deleted=False)
        except Order.DoesNotExist:
            raise serializers.ValidationError("Invalid or inaccessible order.")

        if Payment.objects.filter(order=order, status='completed', is_deleted=False).exists():
            raise serializers.ValidationError("Order already has a completed payment.")

        return data

    def create(self, validated_data):
        order = Order.objects.get(id=validated_data['order']['id'])
        return Payment.objects.create(
            order=order,
            amount=order.total_price,
            payment_method='online',
            status='completed',
            authority_code=str(uuid.uuid4()),
            transaction_id=str(uuid.uuid4()),
            paid_at=timezone.now()
        )