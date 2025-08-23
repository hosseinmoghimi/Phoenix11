from rest_framework import serializers
from .models import Appointment
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer,AccountBriefSerializer,PersonAccountSerializer
from authentication.serializers import PersonSerializer 
 
class AppointmentSerializer(serializers.ModelSerializer):
       person_to_meet=PersonSerializer()
       class Meta:
        model = Appointment
        fields = ['id','title','thumbnail','persian_event_datetime','persian_start_datetime','persian_end_datetime','person_to_meet','get_absolute_url','get_edit_url','get_delete_url']
  