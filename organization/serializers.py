from rest_framework import serializers
from .models import OrganizationUnit
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer,AccountBriefSerializer
 
class OrganizationUnitSerializer(FinancialEventSerializer):
       account=AccountBriefSerializer()
       class Meta:
        model = OrganizationUnit
        fields = ['id','title','account', 'get_absolute_url','get_edit_url','get_delete_url']
 