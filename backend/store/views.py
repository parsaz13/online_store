from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from store.filters import StoreItemFilter
from store.models import Store, StoreItem
from store.permissions import HasStoreOwnerRole, IsOwnerOfStore
from store.serializers import StoreItemSerializer, StoreSerializer


# Store Views
class StoreCreateView(generics.CreateAPIView):
    serializer_class = StoreSerializer
    permission_classes = [HasStoreOwnerRole]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.filter(is_deleted=False)
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated, HasStoreOwnerRole]

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        print("Store destroy called!")
        instance = self.get_object()

        if instance.owner != request.user:
            return Response({'error': 'You do not have permission to delete this store.'}, status=403)

        instance.delete()  
        return Response({'message': 'Store permanently deleted.'}, status=204)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated, HasStoreOwnerRole])
def delete_store(request, pk):
    try:
        store = Store.objects.get(pk=pk)
    except Store.DoesNotExist:
        return Response({'error': 'Store not found.'}, status=404)

    if store.owner != request.user:
        return Response({'error': 'You do not have permission to delete this store.'}, status=403)

    store.is_deleted = True
    store.save()
    return Response({'message': 'Store deleted successfully.'}, status=200)


# StoreItem Views
class StoreItemCreateView(generics.CreateAPIView):
    queryset = StoreItem.objects.all()
    serializer_class = StoreItemSerializer
    permission_classes = [permissions.IsAuthenticated, HasStoreOwnerRole]

    def perform_create(self, serializer):
        try:
            store = Store.objects.get(owner=self.request.user)
            serializer.save(store=store)
        except Store.DoesNotExist:
            return Response({'error': 'You do not have a store.'}, status=400)


class StoreItemListView(generics.ListAPIView):
    serializer_class = StoreItemSerializer
    queryset = StoreItem.objects.filter(is_deleted=False, is_listed=True)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['store', 'price', 'discount_percentage', 'product']
    ordering_fields = ['price', 'discount_percentage', 'created_at']


class StoreItemViewSet(viewsets.ModelViewSet):
    queryset = StoreItem.objects.filter(is_deleted=False)
    serializer_class = StoreItemSerializer
    permission_classes = [permissions.IsAuthenticated, HasStoreOwnerRole]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['price', 'created_at', 'product__name']
    ordering = ['-created_at']
    filterset_class = StoreItemFilter

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def perform_update(self, serializer):
        serializer.save(store=self.request.user.store)
