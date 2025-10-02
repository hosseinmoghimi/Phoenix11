from rest_framework import serializers
from .models import Family
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer,AccountBriefSerializer,PersonAccountSerializer
from authentication.serializers import PersonSerializer 
 
class FamilySerializer(serializers.ModelSerializer):
       father=PersonSerializer()
       mother=PersonSerializer()
       childs=PersonSerializer(many=True)
       class Meta:
        model = Family
        fields = ['id','father','mother','childs','get_absolute_url','get_edit_url','get_delete_url']
  