from django.contrib import admin
from .models import Shop,Customer,Supplier,Shipper,CartItem,Menu,Desk,DeskCustomer

admin.site.register(CartItem)
admin.site.register(Customer)
admin.site.register(Desk)
admin.site.register(DeskCustomer)
admin.site.register(Menu)
admin.site.register(Shop)
admin.site.register(Shipper)
admin.site.register(Supplier)