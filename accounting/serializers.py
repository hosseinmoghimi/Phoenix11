from rest_framework import serializers
from .models import Category,InvoiceLineItem,Account,Service,Product,InvoiceLine,Invoice,FinancialEvent,FinancialDocumentLine,InvoiceLineItemUnit
from .models import FinancialDocument,ProductSpecification,FinancialYear,PersonAccount
from authentication.serializer import PersonSerializer

class AccountSerializer(serializers.ModelSerializer):
       class Meta:
        model = Account
        fields = ['id','name','full_name','logo','code','balance', 'type','color', 'get_absolute_url','get_edit_url','get_delete_url']

class InvoiceSerializer(serializers.ModelSerializer):
       bedehkar=AccountSerializer()
       bestankar=AccountSerializer()
       class Meta:
        model = Invoice
        fields = ['id','title','bedehkar' ,'bestankar','sum_total','amount','persian_event_datetime','get_absolute_url','get_edit_url','get_delete_url']
 
class FinancialYearSerializer(serializers.ModelSerializer): 
    class Meta:
        model = FinancialYear
        fields = ['id','in_progress','name','status','persian_start_date','persian_end_date', 'get_absolute_url','get_edit_url','get_delete_url']


 


class FinancialEventSerializer(serializers.ModelSerializer):
       bedehkar=AccountSerializer()
       bestankar=AccountSerializer()
       class Meta:
        model = FinancialEvent
        fields = ['id','title','bedehkar' ,'bestankar','amount','persian_event_datetime','get_absolute_url','get_edit_url','get_delete_url']

 
 


class ProductSerializer(serializers.ModelSerializer):
       class Meta:
        model = Product
        fields = ['id','title','thumbnail','unit_name','unit_price','barcode',  'get_absolute_url','get_edit_url','get_delete_url']
        # fields = ['id','name','get_market_absolute_url','thumbnail','barcode','unit_price', 'unit_name',  'get_absolute_url','get_edit_url','get_delete_url']


class ServiceSerializer(serializers.ModelSerializer):
       class Meta:
        model = Service
        fields = ['id','title','thumbnail','unit_name','unit_price','get_absolute_url','get_edit_url','get_delete_url']
        # fields = ['id','name','get_market_absolute_url','thumbnail','barcode','unit_price', 'unit_name',  'get_absolute_url','get_edit_url','get_delete_url']

class InvoiceLineItemSerializer(serializers.ModelSerializer):
       class Meta:
              model = InvoiceLineItem
              fields = ['id','title','thumbnail','unit_name','unit_price',  'get_absolute_url','get_edit_url','get_delete_url']
        # fields = ['id','name','get_market_absolute_url','thumbnail','barcode','unit_price', 'unit_name',  'get_absolute_url','get_edit_url','get_delete_url']

class InvoiceLineSerializer(serializers.ModelSerializer):
       invoice_line_item=InvoiceLineItemSerializer()
       class Meta:
        model = InvoiceLine
        fields = ['id','unit_price','row','line_total','quantity','unit_name','discount','discount_percentage',  'invoice_line_item' , 'get_absolute_url','get_edit_url','get_delete_url']

class InvoiceLineWithInvoiceSerializer(InvoiceLineSerializer):
       invoice=InvoiceSerializer()
       class Meta:
        model = InvoiceLine
        fields = ['id','unit_price','invoice','line_total','quantity','unit_name','discount','discount_percentage',  'invoice_line_item' , 'get_absolute_url','get_edit_url','get_delete_url']

class InvoiceLineItemUnitSerializer(serializers.ModelSerializer):
    invoice_line_item=InvoiceLineItemSerializer()
    class Meta:
        model = InvoiceLineItemUnit
        fields = ['id','unit_name','default','unit_price','coef','invoice_line_item','persian_date_added', 'get_edit_url','get_delete_url']
 
  
class AccountBriefSerializer(serializers.ModelSerializer):
       class Meta:
        model = Account
        fields = ['id','parent_id','full_name','logo','name','code','balance', 'type','color', 'get_absolute_url','get_edit_url','get_delete_url']

class FinancialDocumentSerializer(serializers.ModelSerializer):
       class Meta:
        model = FinancialDocument
        fields = ['id','title','balance','bedehkar','bestankar','get_absolute_url','get_edit_url','get_delete_url']



class CategorySerializer(serializers.ModelSerializer):
       class Meta:
        model = Category
        fields = ['id','title','full_title','priority', 'get_absolute_url','get_edit_url','get_delete_url']


class FinancialDocumentLineSerializer(serializers.ModelSerializer):
       financial_event=FinancialEventSerializer()
       financial_document=FinancialDocumentSerializer()
       account=AccountSerializer()
       class Meta:
        model = FinancialDocumentLine
        fields = ['id','account','financial_document','amount','title','persian_date_time','balance','bedehkar','bestankar','financial_event', 'get_absolute_url','get_edit_url','get_delete_url']

class ProductSpecificationSerializer(serializers.ModelSerializer):
    product=ProductSerializer()
    class Meta:
        model = ProductSpecification
        fields = ['id','name','value','product', 'get_edit_url','get_delete_url']

 

class PersonAccountSerializer(serializers.ModelSerializer):
       person=PersonSerializer
       class Meta:
        model = PersonAccount
        fields = ['id','person','name','full_name','logo','code','balance', 'type','color', 'get_absolute_url','get_edit_url','get_delete_url']
