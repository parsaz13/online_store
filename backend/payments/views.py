from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer
from orders.models import Order
from django.utils import timezone
import uuid
from rest_framework import permissions

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'customer'

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.filter(is_deleted=False)
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_queryset(self):
        return self.queryset.filter(order__user=self.request.user)

    def perform_create(self, serializer):
        order_id = self.request.data.get('order_id')
        try:
            order = Order.objects.get(id=order_id, user=self.request.user, is_deleted=False)
            if order.status != 'pending':
                return Response({"error": "Order is not in pending status."}, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"error": "Invalid or inaccessible order."}, status=status.HTTP_404_NOT_FOUND)

        total_price = sum(item.price_at_purchase * item.quantity for item in order.orderitem_set.filter(is_deleted=False))
        serializer.save(
            order=order,
            amount=total_price,
            payment_method='online',
            status='completed',  # فرضاً پرداخت موفق
            authority_code=str(uuid.uuid4()),
            transaction_id=str(uuid.uuid4()),
            paid_at=timezone.now()
        )