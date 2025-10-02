from rest_framework import serializers
from .models import Appointment,Task
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer,AccountBriefSerializer,PersonAccountSerializer
from authentication.serializers import PersonSerializer 
 
class AppointmentSerializer(serializers.ModelSerializer):
       persons_to_meet=PersonSerializer(many=True)
       class Meta:
        model = Appointment
        fields = ['id','title','thumbnail','persian_event_datetime','persian_start_datetime','persian_end_datetime','persons_to_meet','get_absolute_url','get_edit_url','get_delete_url']
  
class TaskSerializer(serializers.ModelSerializer):
       class Meta:
        model = Task
        fields = ['id','title','thumbnail','persian_event_datetime','persian_start_datetime','persian_end_datetime','get_absolute_url','get_edit_url','get_delete_url']
  