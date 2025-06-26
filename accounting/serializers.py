from rest_framework import serializers
from .models import InvoiceLineItem,Account,Product,InvoiceLine,Invoice,FinancialEvent,AccountingDocumentLine,InvoiceLineItemUnit



class AccountSerializer(serializers.ModelSerializer):
       class Meta:
        model = Account
        fields = ['id','name','full_name','logo','code','balance', 'type','color', 'get_absolute_url','get_edit_url','get_delete_url']

class InvoiceSerializer(serializers.ModelSerializer):
       bedehkar=AccountSerializer()
       bestankar=AccountSerializer()
       class Meta:
        model = Invoice
        fields = ['id','title','bedehkar' ,'bestankar','amount','persian_event_datetime','get_absolute_url','get_edit_url','get_delete_url']
 
 

class FinancialEventSerializer(serializers.ModelSerializer):
       bedehkar=AccountSerializer()
       bestankar=AccountSerializer()
       class Meta:
        model = FinancialEvent
        fields = ['id','title','bedehkar' ,'bestankar','amount','persian_event_datetime','get_absolute_url','get_edit_url','get_delete_url']


class AccountingDocumentLineSerializer(serializers.ModelSerializer):
       class Meta:
        model = AccountingDocumentLine
        fields = ['id','get_absolute_url','get_edit_url','get_delete_url']



class ProductSerializer(serializers.ModelSerializer):
       class Meta:
        model = Product
        fields = ['id','title','thumbnail','barcode',  'get_absolute_url','get_edit_url','get_delete_url']
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
        fields = ['id','unit_price','line_total','quantity','unit_name','discount','discount_percentage',  'invoice_line_item' , 'get_absolute_url','get_edit_url','get_delete_url']

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
