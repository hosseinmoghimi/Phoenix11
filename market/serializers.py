from core.serializer import serializers
from .models import Shop,Menu,Supplier,Customer,CartItem,Shipper
from accounting.serializers import Product,AccountBriefSerializer

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id', 'title','thumbnail', 'get_absolute_url','get_edit_url','get_delete_url']
 

 
class ShopSerializer(serializers.ModelSerializer):
    product=ProductSerializer()
    class Meta:
        model=Shop
        fields=['id','unit_price','product','unit_name','quantity','available','persian_start_date', 'get_absolute_url','get_edit_url','get_delete_url']
 


class SupplierSerializer(serializers.ModelSerializer):
    account=AccountBriefSerializer()
    class Meta:
        model=Supplier
        fields=['id','account', 'get_absolute_url', 'get_edit_url','get_delete_url']
 

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
 
