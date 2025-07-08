from rest_framework import serializers
from .models import Food,Meal,FoodItem,MealItem
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer
class FoodItemSerializer(serializers.ModelSerializer):
       class Meta:
        model = FoodItem
        fields = ['id','title','barcode','thumbnail','unit_price','unit_name','get_absolute_url','get_edit_url','get_delete_url']
 
class FoodSerializer(serializers.ModelSerializer):
       items=FoodItemSerializer(many=True)
       class Meta:
        model = Food
        fields = ['id','name','items', 'get_absolute_url','get_edit_url','get_delete_url']
 
class MealSerializer(FinancialEventSerializer):
       class Meta:
        model = Meal
        fields = ['id','title','bedehkar','sum_total','bestankar','amount','persian_event_datetime','get_absolute_url','get_edit_url','get_delete_url']


class MealItemSerializer(InvoiceLineSerializer):
       food_item=FoodItemSerializer()
       class Meta:
        model = MealItem
        fields = ['id','unit_price','discount','quantity','discount_percentage','line_total','unit_name', 'food_item' , 'get_absolute_url','get_edit_url','get_delete_url']



class MealItemWithMealSerializer(InvoiceLineSerializer):
       meal=MealSerializer()
       food_item=FoodItemSerializer()
       class Meta:
        model = MealItem
        fields = ['id','unit_price','quantity','discount_percentage','line_total','unit_name', 'meal','food_item' , 'get_absolute_url','get_edit_url','get_delete_url']
