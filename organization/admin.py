from django.contrib import admin
from .models import OrganizationUnit,Employee

admin.site.register(OrganizationUnit)
# Register your models here.

admin.site.register(Employee)