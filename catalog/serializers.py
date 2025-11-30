from rest_framework import serializers
from .models import Catalog
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer,AccountBriefSerializer,PersonAccountSerializer
from authentication.serializers import PersonSerializer 
 
class CatalogSerializer(serializers.ModelSerializer):
       class Meta:
        model = Catalog
        fields = ['id','title','get_absolute_url','get_edit_url','get_delete_url']
  