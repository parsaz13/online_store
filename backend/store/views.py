from rest_framework import generics, permissions, filters
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from store.models import Store, StoreItem
from store.serializers import StoreSerializer, StoreItemSerializer
from store.filters import StoreItemFilter
from rest_framework.decorators import api_view, permission_classes



# Permissions
class HasStoreOwnerRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'store_owner'


class IsOwnerOfStore(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

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

        instance.delete()  # حذف کامل از دیتابیس
        return Response({'message': 'Store permanently deleted.'}, status=204)


# StoreItem Views
class StoreItemCreateView(generics.CreateAPIView):
    queryset = StoreItem.objects.all()
    serializer_class = StoreItemSerializer
    permission_classes = [permissions.IsAuthenticated, HasStoreOwnerRole]

    def perform_create(self, serializer):
        store = Store.objects.get(owner=self.request.user)
        serializer.save(store=store)



class StoreItemViewSet(viewsets.ModelViewSet):
    queryset = StoreItem.objects.filter(is_deleted=False)
    serializer_class = StoreItemSerializer
    permission_classes = [permissions.IsAuthenticated, HasStoreOwnerRole]
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    ordering_fields = ['price','created_at','product__name']
    ordering = ['-created_at']
    filterset_class = StoreItemFilter

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def perform_update(self, serializer):
        serializer.save(store=self.request.user.store)



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
        store = Store.objects.get(pk=pk)
    except Store.DoesNotExist:
        return Response({'error': 'Store not found.'}, status=404)

    if store.owner != request.user:
        return Response({'error': 'You do not have permission to delete this store.'}, status=403)

    store.is_deleted = True
    store.save()
    return Response({'message': 'Store deleted successfully.'}, status=200)
