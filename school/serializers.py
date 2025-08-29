from rest_framework import serializers
from .models import School,CourseClass,Course,Teacher,Student,Major
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer,AccountBriefSerializer,PersonAccountSerializer
from authentication.serializers import PersonSerializer
class CourseSerializer(serializers.ModelSerializer):
       class Meta:
        model = Course
        fields = ['id','title','thumbnail','get_absolute_url','get_edit_url','get_delete_url']
 
class SchoolSerializer(serializers.ModelSerializer):
       person_account=PersonAccountSerializer()
       class Meta:
        model = School
        fields = ['id','name','person_account', 'get_absolute_url','get_edit_url','get_delete_url']
 
class TeacherSerializer(FinancialEventSerializer):
       person_account=PersonAccountSerializer()
       class Meta:
        model = Teacher
        fields = ['id','person_account', 'get_absolute_url','get_edit_url','get_delete_url']

 
class StudentSerializer(FinancialEventSerializer):
       person_account=PersonAccountSerializer()
       class Meta:
        model = Student
        fields = ['id','person_account', 'get_absolute_url','get_edit_url','get_delete_url']

 

 
class MajorSerializer(FinancialEventSerializer):
       class Meta:
        model = Major
        fields = ['id','title','get_absolute_url','get_edit_url','get_delete_url']

 
class CourseClassSerializer(FinancialEventSerializer):
       major=MajorSerializer()
       school=SchoolSerializer()
       course=CourseSerializer()
       class Meta:
        model = CourseClass
        fields = ['id','school','educational_year','course','level','major','room','get_absolute_url','get_edit_url','get_delete_url']

 