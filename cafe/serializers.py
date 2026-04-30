from rest_framework import serializers
from .models import Table
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer
 
class TableSerializer(serializers.ModelSerializer):
       class Meta:
        model = Table
        fields = ['id','title','table_no', 'get_absolute_url','get_edit_url','get_delete_url']
  