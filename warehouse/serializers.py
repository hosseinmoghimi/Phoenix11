from rest_framework import serializers
from .models import WareHouse
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer,AccountBriefSerializer
from organization.serializers import OrganizationUnitSerializer


class WareHouseSerializer(serializers.ModelSerializer):
       account=AccountBriefSerializer()
       organization_unit=OrganizationUnitSerializer()
       class Meta:
        model = WareHouse
        fields = ['id','name','organization_unit','account', 'get_absolute_url','get_edit_url','get_delete_url']
  