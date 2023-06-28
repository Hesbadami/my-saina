from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(MusicalInstrument)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShoppingCart)
admin.site.register(CartItem)
admin.site.register(ShippingInformation)
