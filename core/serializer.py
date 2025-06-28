from rest_framework import serializers
from .models import Page


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Page
        fields=['id','unit_price', 'get_edit_url','get_delete_url']
 
