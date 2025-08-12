from rest_framework import serializers
from .models import Tax
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer,AccountBriefSerializer,PersonAccountSerializer
from authentication.serializers import PersonSerializer 
 
class TaxSerializer(serializers.ModelSerializer):
       class Meta:
        model = Tax
        fields = ['id','title','get_absolute_url','get_edit_url','get_delete_url']
  