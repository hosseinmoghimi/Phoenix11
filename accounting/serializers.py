from rest_framework import serializers
from .models import Account,Product



class AccountSerializer(serializers.ModelSerializer):
       class Meta:
        model = Account
        fields = ['id','name','full_name','logo','code','balance', 'type','color', 'get_absolute_url','get_edit_url','get_delete_url']

class ProductSerializer(serializers.ModelSerializer):
       class Meta:
        model = Product
        fields = ['id','title','thumbnail','barcode',  'get_absolute_url','get_edit_url','get_delete_url']
        # fields = ['id','name','get_market_absolute_url','thumbnail','barcode','unit_price', 'unit_name',  'get_absolute_url','get_edit_url','get_delete_url']

 