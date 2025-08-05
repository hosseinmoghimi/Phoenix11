from django.contrib import admin
from .models import Vehicle,MaintenanceInvoice,ServiceMan
admin.site.register(Vehicle) 
admin.site.register(MaintenanceInvoice)
admin.site.register(ServiceMan)