from rest_framework import serializers
from .models import Shop


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model=Shop
        fields=['id','unit_price', 'get_edit_url','get_delete_url']
 
