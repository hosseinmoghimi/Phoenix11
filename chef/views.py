from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from .repo import MealRepo,FoodRepo,FoodItemRepo
from .serializers import MealSerializer,FoodSerializer,MealItemSerializer,FoodItemSerializer
from django.views import View
from .forms import *
from .apps import APP_NAME
from core.views import CoreContext
from phoenix.server_apps import phoenix_apps
from utility.calendar import PersianCalendar
import json

LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='chef/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"
 
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context


 
class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        phoenix_apps = sorted(phoenix_apps, key=lambda d: d['priority'])

        context['phoenix_apps']=phoenix_apps
        return render(request,TEMPLATE_ROOT+"index.html",context)
# Create your views here. 

 
 
class FoodsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        foods=FoodRepo(request=request).list(*args, **kwargs)
        context["foods"]=foods

        return render(request,TEMPLATE_ROOT+"foods.html",context)
# Create your views here. 

 
class MealsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        meals=MealRepo(request=request).list(*args, **kwargs)
        meals_s=json.dumps(MealSerializer(meals,many=True).data)
        context["meals_s"]=meals_s
        context["meals"]=meals

        return render(request,TEMPLATE_ROOT+"meals.html",context)
# Create your views here. 



 
class FoodItemView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        food_item=FoodItemRepo(request=request).food_item(*args, **kwargs)
        context["food_item"]=food_item

        meal_items=food_item.mealitem_set.all()
        meal_items_s=json.dumps(MealItemSerializer(meal_items,many=True).data)
        context["meal_items_s"]=meal_items_s
        return render(request,TEMPLATE_ROOT+"food-item.html",context)
# Create your views here. 



 
class FoodView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        food=MealRepo(request=request).list(*args, **kwargs)
        context["food"]=food

        return render(request,TEMPLATE_ROOT+"food.html",context)
# Create your views here. 



 
class MealView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        meal=MealRepo(request=request).meal(*args, **kwargs)
        context["meal"]=meal
        meal_items=meal.mealitem_set.all()
        meal_items_s=json.dumps(MealItemSerializer(meal_items,many=True).data)
        context["meal_items_s"]=meal_items_s
        if True:
            food_items=FoodItemRepo(request=request).list()
            food_items_s=json.dumps(FoodItemSerializer(food_items,many=True).data)
            context["food_items_s"]=food_items_s
        return render(request,TEMPLATE_ROOT+"meal.html",context)
# Create your views here. 

 
class MealItemView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        meal=MealRepo(request=request).meal(*args, **kwargs)
        context["meal"]=meal
        meal_items=meal.mealitem_set.all()
        meal_items_s=json.dumps(MealItemSerializer(meal_items,many=True).data)
        context["meal_items_s"]=meal_items_s

        return render(request,TEMPLATE_ROOT+"meal-item.html",context)
# Create your views here. 

class ReportView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        meals=MealRepo(request=request).list(*args, **kwargs)
        context["meals"]=meals
        ssss=meals[0].persian_datetime()
        meals_s=json.dumps(MealSerializer(meals,many=True).data)
        context["meals_s"]=meals_s
        return render(request,TEMPLATE_ROOT+"report.html",context)
# Create your views here. 
