from rest_framework import serializers
from .models import  Parameter 
# from authentication.serializers import ProfileSerializer



 
class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model=Parameter
        fields=['id','name','app_name','value','get_edit_url','get_delete_url']

