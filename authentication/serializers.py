from rest_framework import serializers
from .models import Profile,Person


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=['id','full_name','username','user_id','image','get_absolute_url', 'get_edit_url','get_delete_url']
 


class PersonSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=Person
        fields=['id','full_name','image','profile','get_absolute_url', 'get_edit_url','get_delete_url']
 
