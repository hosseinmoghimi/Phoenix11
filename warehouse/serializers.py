from rest_framework import serializers
from .models import WareHouse,WareHouseSheet,WareHouseSheetSignature
from accounting.serializers import PersonAccountSerializer,InvoiceLineWithInvoiceSerializer
from authentication.serializers import PersonSerializer
from organization.serializers import EmployeeSerializer

class WareHouseSerializer(serializers.ModelSerializer):
       person_account=PersonAccountSerializer()
       class Meta:
        model = WareHouse
        fields = ['id','name','thumbnail','person_account', 'get_absolute_url','get_edit_url','get_delete_url']
  
class WareHouseSheetSerializer(serializers.ModelSerializer):
       invoice_line=InvoiceLineWithInvoiceSerializer()
       warehouse=WareHouseSerializer()
       person=PersonSerializer()
       class Meta:
        model = WareHouseSheet
        fields = ['id','shelf','col','row','invoice_line','direction','warehouse','persian_date_added','person', 'get_absolute_url','get_edit_url','get_delete_url']
  
class WareHouseSheetSignatureSerializer(serializers.ModelSerializer):
       warehouse_sheet=WareHouseSheetSerializer()
       employee=EmployeeSerializer()
       class Meta:
        model = WareHouseSheetSignature
        fields = ['id', 'warehouse_sheet','status','description','persian_date_added','employee', 'get_edit_url','get_delete_url']
  