from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import Cart, CartItem
from store.models import StoreItem
from users.models import Address
from django.db import transaction
from rest_framework import permissions
class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'customer'

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.filter(is_deleted=False)
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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
                    storeitem.save()
                
                cart_items.delete()  

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        except Cart.DoesNotExist:
            return Response({"error": "Cart does not exist."}, status=status.HTTP_404_NOT_FOUND)