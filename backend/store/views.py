from rest_framework import generics, permissions, filters
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from store.models import Store, StoreItem
from store.serializers import StoreSerializer, StoreItemSerializer
from store.filters import StoreItemFilter



# Permissions
class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "seller"


class IsStoreOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        if hasattr(obj, 'store') and hasattr(obj.store, 'owner'):
            return obj.store.owner == request.user
        return False


# Store Views
class StoreCreateView(generics.CreateAPIView):
    serializer_class = StoreSerializer
    permission_classes = [IsSeller]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.filter(is_deleted=False)
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated, IsStoreOwner]

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return super().get_permissions()



# StoreItem Views
class StoreItemCreateView(generics.CreateAPIView):
    queryset = StoreItem.objects.all()
    serializer_class = StoreItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsSeller]

    def perform_create(self, serializer):
        store = Store.objects.get(owner=self.request.user)
        serializer.save(store=store)



class StoreItemViewSet(viewsets.ModelViewSet):
    queryset = StoreItem.objects.filter(is_deleted=False)
    serializer_class = StoreItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsStoreOwner]
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
    
    