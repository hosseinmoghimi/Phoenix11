from rest_framework import serializers
from .models import page


class pageSerializer(serializers.ModelSerializer):
    class Meta:
        model=page
        fields=['id','unit_price', 'get_edit_url','get_delete_url']
 
