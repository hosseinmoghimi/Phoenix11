from django.contrib import admin
from .models import Shop,Customer,Supplier,Shipper,CartItem

admin.site.register(Shop)
admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Shipper)
admin.site.register(CartItem)