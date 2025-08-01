from rest_framework import serializers
from .models import School,CourseClass,Course
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer,AccountBriefSerializer,PersonAccountSerializer

class CourseSerializer(serializers.ModelSerializer):
       class Meta:
        model = Course
        fields = ['id','title','thumbnail','get_absolute_url','get_edit_url','get_delete_url']
 
class SchoolSerializer(serializers.ModelSerializer):
       person_account=PersonAccountSerializer()
       class Meta:
        model = School
        fields = ['id','name','person_account', 'get_absolute_url','get_edit_url','get_delete_url']
 
class CourseClassSerializer(FinancialEventSerializer):
       class Meta:
        model = CourseClass
        fields = ['id','title','bedehkar','sum_total','bestankar','amount','persian_event_datetime','get_absolute_url','get_edit_url','get_delete_url']

 