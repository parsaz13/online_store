from django.contrib import admin
from .models import Store, StoreItem
# Register your models here.


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "is_deleted", "created_at")
    search_fields = ("name","owner__email")
    list_filter = ("is_deleted",)


@admin.register(StoreItem)
class StoreItemAdmin(admin.ModelAdmin):
    list_display = ("product", "store", "price", "is_deleted")
    search_fields = ("product__name", "store__name")
    list_filter = ("is_deleted",)


