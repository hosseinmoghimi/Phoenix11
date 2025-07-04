from rest_framework import serializers
from .models import Page
from authentication.serializer import ProfileSerializer

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Page
        fields=['id','title','get_absolute_url' ,'get_edit_url','get_delete_url']
 
