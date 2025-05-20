from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=['id','get_absolute_url', 'get_edit_url','get_delete_url']
 
