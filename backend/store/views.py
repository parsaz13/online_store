from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from store.filters import StoreItemFilter
from store.models import Store, StoreItem
from store.permissions import HasStoreOwnerRole
from store.serializers import StoreItemSerializer, StoreSerializer


# Store Views
class StoreCreateView(generics.CreateAPIView):
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated, HasStoreOwnerRole]

    def perform_create(self, serializer):
        if Store.objects.filter(owner=self.request.user, is_deleted=False).exists():
            raise ValidationError("You already have an active store.")
        serializer.save(owner=self.request.user)


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.filter(is_deleted=False)
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated, HasStoreOwnerRole]

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("You are not the owner of this store.")
        instance.is_deleted = True
        instance.save()

    def perform_update(self, serializer):
        if self.get_object().owner != self.request.user:
            raise PermissionDenied("You are not the owner of this store.")
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return super().get_permissions()


# StoreItem Views
class StoreItemCreateView(generics.CreateAPIView):
    queryset = StoreItem.objects.all()
    serializer_class = StoreItemSerializer
    permission_classes = [permissions.IsAuthenticated, HasStoreOwnerRole]

    def perform_create(self, serializer):
        try:
            store = Store.objects.get(owner=self.request.user, is_deleted=False)
        except Store.DoesNotExist:
            raise ValidationError("You do not have an active store.")
        serializer.save(store=store)


class StoreItemViewSet(viewsets.ModelViewSet):
    queryset = StoreItem.objects.filter(is_deleted=False)
    serializer_class = StoreItemSerializer
    permission_classes = [permissions.IsAuthenticated, HasStoreOwnerRole]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['price', 'created_at', 'product__name']
    ordering = ['-created_at']
    filterset_class = StoreItemFilter

    def perform_destroy(self, instance):
        if instance.store.owner != self.request.user:
            raise PermissionDenied("You are not the owner of this store item.")
        instance.is_deleted = True
        instance.save()

    def perform_update(self, serializer):
        if self.get_object().store.owner != self.request.user:
            raise PermissionDenied("You are not the owner of this store item.")
        serializer.save()


class StoreItemListView(generics.ListAPIView):
    serializer_class = StoreItemSerializer
    queryset = StoreItem.objects.filter(is_deleted=False, is_listed=True)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['store', 'price', 'discount_percentage', 'product']
    ordering_fields = ['price', 'discount_percentage', 'created_at']


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated, HasStoreOwnerRole])
def delete_store(request, pk):
    try:
        store = Store.objects.get(pk=pk, is_deleted=False)
    except Store.DoesNotExist:
        return Response({'error': 'Store not found.'}, status=status.HTTP_404_NOT_FOUND)

    if store.owner != request.user:
        return Response({'error': 'You do not have permission to delete this store.'}, status=status.HTTP_403_FORBIDDEN)

    store.is_deleted = True
    store.save()
    return Response({'message': 'Store deleted successfully.'}, status=status.HTTP_200_OK)
