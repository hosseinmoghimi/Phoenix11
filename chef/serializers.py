from rest_framework import serializers
from .models import Food,Meal,FoodItem,MealItem

class FoodItemSerializer(serializers.ModelSerializer):
       class Meta:
        model = FoodItem
        fields = ['id','name','price','get_absolute_url','get_edit_url','get_delete_url']
 
class FoodSerializer(serializers.ModelSerializer):
       items=FoodItemSerializer(many=True)
       class Meta:
        model = Food
        fields = ['id','name','items', 'get_absolute_url','get_edit_url','get_delete_url']

class MealSerializer(serializers.ModelSerializer):
       class Meta:
        model = Meal
        fields = ['id','name', 'persian_datetime' , 'get_absolute_url','get_edit_url','get_delete_url']

class MealItemSerializer(serializers.ModelSerializer):
       meal=MealSerializer()
       food_item=FoodItemSerializer()
       class Meta:
        model = MealItem
        fields = ['id','price','quantity', 'meal','food_item' , 'get_absolute_url','get_edit_url','get_delete_url']
