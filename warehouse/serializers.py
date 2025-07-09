from rest_framework import serializers
from .models import WareHouse
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer,AccountBriefSerializer
 
class WareHouseSerializer(serializers.ModelSerializer):
       account=AccountBriefSerializer()
       class Meta:
        model = WareHouse
        fields = ['id','name','account', 'get_absolute_url','get_edit_url','get_delete_url']
  