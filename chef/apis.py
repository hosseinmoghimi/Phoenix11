
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import MealRepo,MealItemRepo,FoodRepo,FoodItemRepo
from .serializers import MealSerializer,MealItemSerializer,FoodSerializer,FoodItemSerializer
from django.http import JsonResponse
from .forms import *
   

class AddMealItemApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
        add_meal_item_form=AddMealItemForm(request.POST)
        if add_meal_item_form.is_valid():
            log=333
            cd=add_meal_item_form.cleaned_data
            result,message,meal_item=MealItemRepo(request=request).add_meal_item(**cd)
            if meal_item is not None:
                context['meal_item']=MealItemSerializer(meal_item).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 
class AddMealApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
        add_meal_form=AddMealForm(request.POST)
        if add_meal_form.is_valid():
            log=333
            cd=add_meal_form.cleaned_data
            result,message,meal=MealRepo(request=request).add_meal(**cd)
            if meal is not None:
                context['meal']=MealSerializer(meal).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 