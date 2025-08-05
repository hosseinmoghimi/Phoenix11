from rest_framework import serializers
from .models import Drug
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer
class DrugSerializer(serializers.ModelSerializer):
       class Meta:
        model = Drug
        fields = ['id','title','barcode','thumbnail','unit_price','unit_name','get_absolute_url','get_edit_url','get_delete_url']
  