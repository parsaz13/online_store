from rest_framework import generics, permissions
from rest_framework import viewsets
from store.models import Store, StoreItem
from store.serializers import StoreSerializer, StoreItemSerializer


class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "seller"


class StoreCreateView(generics.CreateAPIView):
    serializer_class = StoreSerializer
    permission_classes = [IsSeller]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class IsStoreOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


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


class StoreItemCreateView(generics.CreateAPIView):
    serializer_class = StoreItemSerializer
    permission_classes = [IsSeller]

    def perform_create(self, serializer):
        serializer.save(store=self.request.user.store)
    


class StoreItemViewSet(viewsets.ModelViewSet):
    queryset = StoreItem.objects.filter(is_deleted=False)
    serializer_class = StoreItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsStoreOwner]
    
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
    
    
    def perform_update(self, serializer):
        serializer.save(store=self.request.user.store) 