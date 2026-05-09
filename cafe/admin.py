from django.contrib import admin
from .models import Table,Menu,Desk,DeskCustomer
 
admin.site.register(Desk)
admin.site.register(DeskCustomer)
admin.site.register(Menu)
admin.site.register(Table)