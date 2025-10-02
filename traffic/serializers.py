from rest_framework import serializers
from .models import Traffic
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer,AccountBriefSerializer,PersonAccountSerializer
from authentication.serializers import PersonSerializer
from attachments.serializer import LocationSerializer 
 
class TrafficSerializer(serializers.ModelSerializer):
       person=PersonSerializer()
       location=LocationSerializer()
       class Meta:
        model = Traffic
        fields = ['id','person','location','persian_enter_datetime','persian_exit_datetime','get_absolute_url','get_edit_url','get_delete_url']
  