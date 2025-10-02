from django.contrib import admin
from .models import Drug,Doctor,Patient,Prescription,PrescriptionLine

admin.site.register(Drug) 
admin.site.register(Doctor) 
admin.site.register(Patient) 
admin.site.register(Prescription) 
admin.site.register(PrescriptionLine) 