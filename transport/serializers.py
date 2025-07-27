from core.serializers import serializers
from .models import Vehicle,MaintenanceInvoice

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vehicle
        fields=['id', 'title','thumbnail','get_absolute_url',  'get_edit_url','get_delete_url']
  

class MaintenanceInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=MaintenanceInvoice
        fields=['id', 'title','thumbnail','get_absolute_url',  'get_edit_url','get_delete_url']
 
 