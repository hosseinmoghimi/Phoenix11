from rest_framework import serializers
from .models import  Parameter,MyLink
from attachments.serializer import PersonSerializer,LinkSerializer



 
class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model=Parameter
        fields=['id','name','app_name','value','get_edit_url','get_delete_url']

 
class MyLinkSerializer(serializers.ModelSerializer):
    person=PersonSerializer()
    class Meta:
        model=MyLink
        fields=['id','person','title','url','priority']

