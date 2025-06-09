from rest_framework import serializers
from .models import Account,Product,Invoice,FinancialEvent,AccountingDocumentLine



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

 