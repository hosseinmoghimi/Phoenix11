from rest_framework import serializers
from .models import Sample
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer,AccountBriefSerializer,PersonAccountSerializer
from authentication.serializers import PersonSerializer 
 
class SampleSerializer(serializers.ModelSerializer):
       class Meta:
        model = Sample
        fields = ['id','title','get_absolute_url','get_edit_url','get_delete_url']
  