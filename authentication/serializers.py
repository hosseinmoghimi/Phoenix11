from rest_framework import serializers
from .models import Person




class PersonSerializer(serializers.ModelSerializer): 
    
    class Meta:
        model=Person
        fields=['id','full_name','image','username','user_id','get_absolute_url', 'get_edit_url','get_delete_url']
 

class ProfileSerializer(PersonSerializer):
    pass