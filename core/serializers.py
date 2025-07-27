from rest_framework import serializers
from .models import Page
from authentication.serializers import ProfileSerializer

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Page
        fields=['id','title','app_name','class_title','get_absolute_url' ,'get_edit_url','get_delete_url']
 

class PageBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model=Page
        fields=['id','title','app_name','class_title','get_edit_url','get_delete_url', 'thumbnail','get_absolute_url' ]
 
