from rest_framework import serializers
from .models import WareHouse
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer,AccountBriefSerializer
from organization.serializers import OrganizationUnitSerializer
from accounting.serializers import PersonAccountSerializer


class WareHouseSerializer(serializers.ModelSerializer):
       person_account=PersonAccountSerializer()
       class Meta:
        model = WareHouse
        fields = ['id','name','thumbnail','person_account', 'get_absolute_url','get_edit_url','get_delete_url']
  