from rest_framework import serializers
from .models import Poll
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer,AccountBriefSerializer,PersonAccountSerializer
from authentication.serializers import PersonSerializer 
 
class PollSerializer(serializers.ModelSerializer):
       class Meta:
        model = Poll
        fields = ['id','title','get_absolute_url','get_edit_url','get_delete_url']
  