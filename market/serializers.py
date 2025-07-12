from core.serializer import serializers
from .models import Shop,Menu,Supplier,Customer,CartItem,Shipper,Desk,DeskCustomer
from accounting.serializers import Category,Product,AccountBriefSerializer,PersonSerializer

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id', 'title','unit_name','unit_price','thumbnail','get_market_absolute_url',  'get_edit_url','get_delete_url']
 

 

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id', 'title','thumbnail','get_market_absolute_url',  'get_edit_url','get_delete_url']
 
class SupplierSerializer(serializers.ModelSerializer):
    account=AccountBriefSerializer()
    person=PersonSerializer()
    class Meta:
        model=Supplier
        fields=['id','account','person','full_name','level', 'get_absolute_url', 'get_edit_url','get_delete_url']
 
 


 
class ShopSerializer(serializers.ModelSerializer):
    product=ProductSerializer()
    supplier=SupplierSerializer()
    product=ProductSerializer()
    class Meta:
        model=Shop
        fields=['id','supplier','level','discount_percentage','unit_price','product','unit_name','quantity','available','persian_start_date','persian_end_date', 'get_absolute_url','get_edit_url','get_delete_url']
 

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields=['id','title', 'get_absolute_url','get_edit_url','get_delete_url']
 

class ShipperSerializer(serializers.ModelSerializer):
    class Meta:
        model=Shipper
        fields=['id','title', 'get_absolute_url','get_edit_url','get_delete_url']
 




class MenuSerializer(serializers.ModelSerializer):
    supplier=SupplierSerializer()
    shops=ShopSerializer(many=True)
    class Meta:
        model=Menu
        fields=['id','title','supplier','shops', 'get_absolute_url', 'get_edit_url','get_delete_url']
 




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
 
