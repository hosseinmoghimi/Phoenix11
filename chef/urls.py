from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  

    path('foods/',login_required(views.FoodsView.as_view()),name="foods"),  
    path('meals/',login_required(views.MealsView.as_view()),name="meals"),  
    path('report/',login_required(views.ReportView.as_view()),name="report"),  

    path('add-meal',login_required(apis.AddMealApi.as_view()),name="add_meal"),
    path('add-meal-item',login_required(apis.AddMealItemApi.as_view()),name="add_meal_item"),
    path('food/<int:pk>/',login_required(views.FoodView.as_view()),name="food"),  
    path('food-item/<int:pk>/',login_required(views.FoodItemView.as_view()),name="fooditem"),  
    path('meal/<int:pk>/',login_required(views.MealView.as_view()),name="meal"),  
    path('meal-item/<int:pk>/',login_required(views.MealItemView.as_view()),name="mealitem"),  
]
