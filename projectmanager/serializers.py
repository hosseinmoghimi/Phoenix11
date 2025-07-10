from rest_framework import serializers
from .models import Project,RemoteClient
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer
from organization.serializers import OrganizationUnitSerializer
class ProjectSerializer(FinancialEventSerializer):
       contractor=OrganizationUnitSerializer()
       employer=OrganizationUnitSerializer()
       class Meta:
        model = Project
        fields = ['id','title','thumbnail','employer','contractor', 'get_absolute_url','get_edit_url','get_delete_url']
 
class RemoteClientSerializer(serializers.ModelSerializer):
    class Meta:
        model=RemoteClient
        fields=['id', 'name','get_project_absolute_url','get_project_title', 'get_absolute_url', 'get_edit_url','remote_ip','any_desk_address'
                ,'any_desk_password','username','password','identity','ssid','preshared_key','local_ip'
                ,'frequency','protocol','channel_width','adsl_username','adsl_password',
                'telephone','contact'] 
