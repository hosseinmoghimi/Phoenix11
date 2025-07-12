from core.serializer import serializers
from .models import Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vehicle
        fields=['id', 'title','thumbnail','get_absolute_url',  'get_edit_url','get_delete_url']
 
 