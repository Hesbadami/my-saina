from django.contrib import admin
from .models import *


# Register your models here.

class CartItemAdmin(admin.StackedInline):
    model = CartItem
    extra = 0


class OrderItemAdmin(admin.StackedInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemAdmin, ]


class ShoppingCartAdmin(admin.ModelAdmin):
    inlines = [CartItemAdmin, ]


class MusicalInstrumentAdmin(admin.ModelAdmin):
    list_display = ("instrument_name", "instrument_price", "manufacturer", "category", "available",)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


class CategoryAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


class ManufacturerAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


admin.site.register(Customer)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(MusicalInstrument, MusicalInstrumentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
