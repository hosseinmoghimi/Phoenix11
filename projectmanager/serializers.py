from rest_framework import serializers
from .models import Project
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer
 
class ProjectSerializer(FinancialEventSerializer):
       class Meta:
        model = Project
        fields = ['id','title', 'get_absolute_url','get_edit_url','get_delete_url']
 