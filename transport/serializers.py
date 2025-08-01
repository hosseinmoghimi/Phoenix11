from core.serializers import serializers
from .models import Vehicle,MaintenanceInvoice,ServiceMan
from accounting.serializers import PersonAccountSerializer,AccountBriefSerializer,InvoiceSerializer
class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vehicle
        fields=['id', 'title','thumbnail','get_absolute_url',  'get_edit_url','get_delete_url']
  
 

class ServiceManSerializer(serializers.ModelSerializer):
    person_account=PersonAccountSerializer()
    class Meta:
        model=ServiceMan
        fields=['id', 'title','person_account','get_absolute_url',  'get_edit_url','get_delete_url']
 
 

class MaintenanceInvoiceSerializer(InvoiceSerializer):
    # bedehkar=AccountBriefSerializer()
    # bestankar=AccountBriefSerializer()
    service_man=ServiceManSerializer()
    vehicle=VehicleSerializer()
    class Meta:
        model=MaintenanceInvoice
        fields = ['id','title','vehicle','service_man','bedehkar' ,'bestankar','sum_total','amount','persian_event_datetime','get_absolute_url','get_edit_url','get_delete_url']
 
