from django.contrib import admin
from .models import Ticket,Project,MaterialRequest,ServiceRequest,RemoteClient

admin.site.register(RemoteClient)
admin.site.register(Project)
admin.site.register(MaterialRequest)
admin.site.register(ServiceRequest)
admin.site.register(Ticket)
# Register your models here.
