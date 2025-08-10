from rest_framework import serializers
from .models import Project,RemoteClient
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer,BrandSerializer,ProductSerializer
from organization.serializers import OrganizationUnitSerializer

class ProjectSerializer(FinancialEventSerializer):
       contractor=OrganizationUnitSerializer()
       employer=OrganizationUnitSerializer()
       class Meta:
        model = Project
        fields = ['id','percentage_completed','amount','weight','title','thumbnail','persian_start_datetime','persian_end_datetime','employer','contractor', 'get_absolute_url','get_edit_url','get_delete_url']
 

  
class ProjectSerializerForGuantt(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields=['id','title','get_status_color','color','start_datetime','end_datetime','status','amount','get_absolute_url','short_description','thumbnail','percentage_completed']



class RemoteClientSerializer(serializers.ModelSerializer):
    brand=BrandSerializer()
    product=ProductSerializer()
    class Meta:
        model=RemoteClient
        fields=['id','brand','product', 'name','get_project_absolute_url','get_project_title', 'get_absolute_url', 'get_edit_url','remote_ip','any_desk_address'
                ,'any_desk_password','username','password','identity','ssid','preshared_key','local_ip'
                ,'frequency','protocol','channel_width','adsl_username','adsl_password',
                'telephone','contact'] 
