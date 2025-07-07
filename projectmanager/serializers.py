from rest_framework import serializers
from .models import Project
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer
from organization.serializers import OrganizationSerializer
class ProjectSerializer(FinancialEventSerializer):
       contractor=OrganizationSerializer()
       employer=OrganizationSerializer()
       class Meta:
        model = Project
        fields = ['id','title','employer','contractor', 'get_absolute_url','get_edit_url','get_delete_url']
 