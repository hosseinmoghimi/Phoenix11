from rest_framework import serializers
from .models import Organization
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer
 
class OrganizationSerializer(FinancialEventSerializer):
       class Meta:
        model = Organization
        fields = ['id','title', 'get_absolute_url','get_edit_url','get_delete_url']
 