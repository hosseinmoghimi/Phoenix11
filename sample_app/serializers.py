from rest_framework import serializers
from .models import SampleClass
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer,AccountBriefSerializer,PersonAccountSerializer
from authentication.serializers import PersonSerializer 
 
class SampleClassSerializer(serializers.ModelSerializer):
       class Meta:
        model = SampleClass
        fields = ['id','title','get_absolute_url','get_edit_url','get_delete_url']
  