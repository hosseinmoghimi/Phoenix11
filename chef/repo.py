from .models import Meal,Food,FoodItem,MealItem
from .apps import APP_NAME
from .enums import *
from log.repo import LogRepo 
from django.db.models import Q
from django.shortcuts import reverse
from authentication.repo import ProfileRepo
from utility.num import filter_number
from utility.calendar import PersianCalendar
from utility.constants import FAILED,SUCCEED
from utility.log import leolog
from .enums import *


class FoodRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Food.objects.filter(id=0)
        profile=ProfileRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=Food.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def food(self,*args, **kwargs):
        if "food_id" in kwargs and kwargs["food_id"] is not None:
            return self.objects.filter(pk=kwargs['food_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_food(self,*args,**kwargs):
        result,message,food=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_food"):
            message="دسترسی غیر مجاز"
            return result,message,food

        food=Food()
        if 'name' in kwargs:
            food.name=kwargs["name"]
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                food.parent_id=kwargs["parent_id"]
        if 'color' in kwargs:
            food.color=kwargs["color"]
        if 'code' in kwargs:
            food.code=kwargs["code"]
        if 'priority' in kwargs:
            food.priority=kwargs["priority"]
        if 'type' in kwargs:
            food.type=kwargs["type"]

            
        if 'parent_code' in kwargs:
            parent_code= kwargs["parent_code"]
            parent=Account.objects.filter(code=parent_code).first()
            if parent is not None:
                food.parent_id=parent.id

        if 'nature' in kwargs:
            food.nature=kwargs["nature"]
        (result,message,food)=food.save()
        return result,message,food




class FoodItemRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=FoodItem.objects.filter(id=0)
        profile=ProfileRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=FoodItem.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def food_item(self,*args, **kwargs):
        if "food_item_id" in kwargs and kwargs["food_item_id"] is not None:
            return self.objects.filter(pk=kwargs['food_item_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_food_item(self,*args,**kwargs):
        result,message,food=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_food"):
            message="دسترسی غیر مجاز"
            return result,message,food

        food=Food()
        if 'name' in kwargs:
            food.name=kwargs["name"]
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                food.parent_id=kwargs["parent_id"]
        if 'color' in kwargs:
            food.color=kwargs["color"]
        if 'code' in kwargs:
            food.code=kwargs["code"]
        if 'priority' in kwargs:
            food.priority=kwargs["priority"]
        if 'type' in kwargs:
            food.type=kwargs["type"]

            
        if 'parent_code' in kwargs:
            parent_code= kwargs["parent_code"]
            parent=Account.objects.filter(code=parent_code).first()
            if parent is not None:
                food.parent_id=parent.id

        if 'nature' in kwargs:
            food.nature=kwargs["nature"]
        (result,message,food)=food.save()
        return result,message,food




class MealRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Meal.objects.filter(id=0)
        profile=ProfileRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=Meal.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def meal(self,*args, **kwargs):
        if "meal_id" in kwargs and kwargs["meal_id"] is not None:
            return self.objects.filter(pk=kwargs['meal_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_meal(self,*args,**kwargs):
        result,message,meal=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_meal"):
            message="دسترسی غیر مجاز"
            return result,message,meal

        meal=Meal()
        if 'name' in kwargs:
            meal.name=kwargs["name"]
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                meal.parent_id=kwargs["parent_id"]
        if 'color' in kwargs:
            meal.color=kwargs["color"]
        if 'code' in kwargs:
            meal.code=kwargs["code"]
        if 'priority' in kwargs:
            meal.priority=kwargs["priority"]
        if 'type' in kwargs:
            meal.type=kwargs["type"]

             

        if 'nature' in kwargs:
            meal.nature=kwargs["nature"]
        (result,message,meal)=meal.save()
        return result,message,meal



class MealItemRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=MealItem.objects.filter(id=0)
        profile=ProfileRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=MealItem.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def meal_item(self,*args, **kwargs):
        if "meal_item_id" in kwargs and kwargs["meal_item_id"] is not None:
            return self.objects.filter(pk=kwargs['meal_item_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_meal_item(self,*args,**kwargs):
        result,message,meal=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_meal"):
            message="دسترسی غیر مجاز"
            return result,message,meal

        meal_item=MealItem()
        if 'food_item_id' in kwargs:
            meal_item.food_item_id=kwargs["food_item_id"]
        if 'meal_id' in kwargs:
            if kwargs["meal_id"]>0:
                meal_item.meal_id=kwargs["meal_id"]
        if 'quantity' in kwargs:
            meal_item.quantity=kwargs["quantity"]
        if 'price' in kwargs:
            meal_item.price=kwargs["price"]
        

        result=SUCCEED
        message="آیتم وعده با موفقیت اضافه شد."     
 
        meal_item.save()
        return result,message,meal_item
