from rest_framework import serializers
from .models import Book
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer,AccountBriefSerializer,PersonAccountSerializer
from authentication.serializers import PersonSerializer 
 
class BookSerializer(serializers.ModelSerializer):
       class Meta:
        model = Book
        fields = ['id','title','get_absolute_url','get_edit_url','get_delete_url']
  