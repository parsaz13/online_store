from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from store.models import StoreItem
from users.models import CustomUser

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'customer'

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.filter(is_deleted=False)
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='add-item')
    def add_item(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user, is_deleted=False)
        storeitem_id = request.data.get('storeitem_id')
        quantity = request.data.get('quantity', 1)

        try:
            storeitem = StoreItem.objects.get(id=storeitem_id, is_deleted=False, is_listed=True)
            if storeitem.quantity < quantity:
                return Response({"error": f"Only {storeitem.quantity} items available."}, status=status.HTTP_400_BAD_REQUEST)
        except StoreItem.DoesNotExist:
            return Response({"error": "StoreItem does not exist."}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, storeitem=storeitem, defaults={'quantity': quantity, 'price_at_time': storeitem.final_price}
        )
        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > storeitem.quantity:
                return Response({"error": f"Only {storeitem.quantity} items available."}, status=status.HTTP_400_BAD_REQUEST)
            cart_item.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='update-item')
    def update_item(self, request, pk=None):
        cart = self.get_object()
        cart_item_id = request.data.get('cart_item_id')
        quantity = request.data.get('quantity')

        try:
            cart_item = CartItem.objects.get(id=cart_item_id, cart=cart, is_deleted=False)
            if quantity <= 0:
                cart_item.delete()
                return Response({"message": "Item removed from cart."}, status=status.HTTP_204_NO_CONTENT)
            if cart_item.storeitem.quantity < quantity:
                return Response({"error": f"Only {cart_item.storeitem.quantity} items available."}, status=status.HTTP_400_BAD_REQUEST)
            cart_item.quantity = quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            return Response({"error": "CartItem does not exist."}, status=status.HTTP_404_NOT_FOUND)

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='remove-item')
    def remove_item(self, request, pk=None):
        cart = self.get_object()
        cart_item_id = request.data.get('cart_item_id')

        try:
            cart_item = CartItem.objects.get(id=cart_item_id, cart=cart, is_deleted=False)
            cart_item.delete()
        except CartItem.DoesNotExist:
            return Response({"error": "CartItem does not exist."}, status=status.HTTP_404_NOT_FOUND)

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)