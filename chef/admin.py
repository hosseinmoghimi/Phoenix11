from django.contrib import admin
from .models import Food,FoodItem,Meal,MealItem

admin.site.register(Food)
admin.site.register(FoodItem)
admin.site.register(Meal)
admin.site.register(MealItem)