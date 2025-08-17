from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.db import transaction
from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import Cart, CartItem
from users.models import Address
from store.tasks import send_order_confirmation_email

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'customer'

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.filter(is_deleted=False)
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == "customer":
            return Order.objects.filter(user=user, is_deleted=False)
        elif user.role == "store_owner":
            return Order.objects.filter(orderitem__storeitem__store__owner=user, is_deleted=False).distinct()
        return Order.objects.none()

    def get_permissions(self):
        if self.action in ["list", "retrieve", "update_status"]:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsCustomer()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def update_status(self, request, pk=None):
        order = self.get_object()
        if request.user.role != "store_owner":
            raise PermissionDenied("Only sellers can update order status.")
        status_choice = request.data.get("status")
        if status_choice not in ["pending", "shipped", "delivered"]:
            return Response({"error": "Invalid status."}, status=400)
        order.status = status_choice
        order.save()
        return Response({"message": f"Order status updated to {status_choice}"})

    @action(detail=False, methods=['post'], url_path='create-from-cart')
    def create_from_cart(self, request):
        try:
            cart = Cart.objects.get(user=request.user, is_deleted=False)
            cart_items = CartItem.objects.filter(cart=cart, is_deleted=False)
            if not cart_items.exists():
                return Response({"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

            address_id = request.data.get('address_id')
            try:
                address = Address.objects.get(id=address_id, user=request.user, is_deleted=False)
            except Address.DoesNotExist:
                return Response({"error": "Invalid or inaccessible address."}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                order = Order.objects.create(user=request.user, address=address, status='pending')
                for cart_item in cart_items:
                    storeitem = cart_item.storeitem
                    if storeitem.quantity < cart_item.quantity:
                        return Response({"error": f"Only {storeitem.quantity} of {storeitem.product.title} available."}, status=status.HTTP_400_BAD_REQUEST)
                    
                    OrderItem.objects.create(
                        order=order,
                        storeitem=storeitem,
                        quantity=cart_item.quantity,
                        price_at_purchase=storeitem.final_price
                    )
                    storeitem.quantity -= cart_item.quantity
                    storeitem.sales_count += cart_item.quantity
                    storeitem.save()

                cart_items.update(is_deleted=True)

            send_order_confirmation_email.delay(request.user.email, order.id)

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        except Cart.DoesNotExist:
            return Response({"error": "Cart does not exist."}, status=status.HTTP_404_NOT_FOUND)
