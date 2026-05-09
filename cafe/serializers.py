from rest_framework import serializers
from .models import Table,Desk,DeskCustomer,Menu,MenuItem
from accounting.serializers import AccountBriefSerializer
from market.serializers import SupplierSerializer,ShopSerializer
 
class TableSerializer(serializers.ModelSerializer):
       class Meta:
        model = Table
        fields = ['id','title','table_no', 'get_absolute_url','get_edit_url','get_delete_url']
  
class DeskSerializer(serializers.ModelSerializer):
    supplier=SupplierSerializer()
    class Meta:
        model=Desk 
        fields=['id','code','title','supplier',  'get_absolute_url', 'get_edit_url','get_delete_url']
 

class DeskCustomerSerializer(serializers.ModelSerializer):
    account=AccountBriefSerializer()
    desk=DeskSerializer()
    class Meta:
        model=DeskCustomer 
        fields=['id','desk','account',  'get_absolute_url', 'get_edit_url','get_delete_url']
 
class MenuSerializer(serializers.ModelSerializer):
    supplier=SupplierSerializer()
    shops=ShopSerializer(many=True)
    class Meta:
        model=Menu
        fields=['id','title','supplier','shops', 'get_absolute_url', 'get_edit_url','get_delete_url']



class MenuItemSerializer(serializers.ModelSerializer):
    shop=ShopSerializer()
    class Meta:
        model=MenuItem
        fields=['id','shop','in_cart']

