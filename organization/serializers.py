from rest_framework import serializers
from .models import OrganizationUnit,Employee
from accounting.serializers import PersonAccountSerializer,PersonSerializer,FinancialEventSerializer,InvoiceLineSerializer,AccountBriefSerializer
 
class OrganizationUnitSerializer(FinancialEventSerializer):
       person_account=AccountBriefSerializer()
       class Meta:
        model = OrganizationUnit
        fields = ['id','title','person_account','thumbnail', 'get_absolute_url','get_edit_url','get_delete_url']
 
 
class EmployeeSerializer(FinancialEventSerializer):
       organization_unit=OrganizationUnitSerializer()
       person_account=PersonAccountSerializer()
       class Meta:
        model = Employee
        fields = ['id','person_account','job_title','organization_unit','get_absolute_url','get_edit_url','get_delete_url']
 