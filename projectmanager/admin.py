from django.contrib import admin
from .models import Project,MaterialRequest,ServiceRequest,RemoteClient

admin.site.register(RemoteClient)
admin.site.register(Project)
admin.site.register(MaterialRequest)
admin.site.register(ServiceRequest)
# Register your models here.
