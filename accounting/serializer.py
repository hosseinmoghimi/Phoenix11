from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields=['id','get_absolute_url', 'get_edit_url','get_delete_url']
 
