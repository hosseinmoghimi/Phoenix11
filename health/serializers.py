from rest_framework import serializers
from .models import Drug,Patient,Doctor,Prescription
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer,PersonAccountSerializer,AccountSerializer
class DrugSerializer(serializers.ModelSerializer):
       class Meta:
        model = Drug
        fields = ['id','title','barcode','thumbnail','unit_price','unit_name','get_absolute_url','get_edit_url','get_delete_url']
class PatientSerializer(serializers.Serializer):
       person_account=PersonAccountSerializer()
       class Meta:
        model = Patient
        fields = ['id','person_account', 'get_absolute_url','get_edit_url','get_delete_url']

 
class DoctorSerializer(serializers.Serializer):
       person_account=PersonAccountSerializer()
       class Meta:
        model = Doctor
        fields = ['id','person_account', 'get_absolute_url','get_edit_url','get_delete_url']

 
class PrescriptionSerializer(serializers.Serializer): 
       bedehkar=AccountSerializer()
       bestankar=AccountSerializer()
       class Meta:
        model = Prescription
        fields = ['id','title','thumbnail','bedehkar' ,'bestankar','amount','amount','shipping_fee','persian_event_datetime','get_absolute_url','get_edit_url','get_delete_url']
 
