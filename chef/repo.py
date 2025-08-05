from .models import Meal,Food,FoodItem,MealItem
from .apps import APP_NAME
from .enums import *
from log.repo import LogRepo 
from django.db.models import Q
from django.shortcuts import reverse
from authentication.repo import PersonRepo
from accounting.repo import InvoiceLineItemUnitRepo
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
        profile=PersonRepo(request=request).me
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
        profile=PersonRepo(request=request).me
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
        if "meal_id" in kwargs:
            meal_id=kwargs["meal_id"]
            objects=objects.filter(meal_id=meal_id)  
        return objects.all()
        
    def food_item(self,*args, **kwargs):
        if "food_item_id" in kwargs and kwargs["food_item_id"] is not None:
            return self.objects.filter(pk=kwargs['food_item_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_food_item(self,*args,**kwargs):
        result,message,food_item=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_fooditem"):
            message="دسترسی غیر مجاز"
            return result,message,food_item
         
        food_item=FoodItem()

        if 'barcode' in kwargs:
            food_item.barcode=kwargs["barcode"]
        if 'priority' in kwargs and kwargs['priority'] is not None:
            food_item.priority=kwargs["priority"]
        if 'title' in kwargs:
            food_item.title=kwargs["title"]

          
 
        (result,message,food_item)=food_item.save()

        
        if 'unit_price' in kwargs:
            if 'unit_name' in kwargs:
                if 'coef' in kwargs:
                    from accounting.models import InvoiceLineItemUnit
                    ili_unit=InvoiceLineItemUnit()
                    ili_unit.unit_name=kwargs["unit_name"]
                    ili_unit.coef=kwargs["coef"]
                    ili_unit.unit_price=kwargs["unit_price"]
                    ili_unit.invoice_line_item_id=food_item.id
                    ili_unit.default=True
                    ili_unit.save()

        return result,message,food_item




class MealRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Meal.objects.filter(id=0)
        profile=PersonRepo(request=request).me
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
        if 'bedehkar_id' in kwargs:
            meal.bedehkar_id=kwargs["bedehkar_id"]
        if 'bestankar_id' in kwargs:
            meal.bestankar_id=kwargs["bestankar_id"]
        if 'code' in kwargs:
            meal.code=kwargs["code"]
        if 'event_datetime' in kwargs:
            meal.event_datetime=kwargs["event_datetime"]
            meal.event_datetime=kwargs["event_datetime"]
            year=kwargs['event_datetime'][:2]
            if year=="13" or year=="14":
                kwargs['event_datetime']=PersianCalendar().to_gregorian(kwargs["event_datetime"])
            meal.event_datetime=kwargs['event_datetime']


        if 'title' in kwargs:
            meal.title=kwargs["title"]
        
        (result,message,meal)=meal.save()
        return result,message,meal



class MealItemRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=MealItem.objects.filter(id=0)
        profile=PersonRepo(request=request).me
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
        if "food_item_id" in kwargs:
            food_item_id=kwargs["food_item_id"]
            objects=objects.filter(invoice_line_item_id=food_item_id)  
        if "meal_id" in kwargs:
            meal_id=kwargs["meal_id"]
            invoice_id=kwargs["meal_id"]
            objects=objects.filter(invoice_id=invoice_id)  

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
            invoice_line_item_id=kwargs["food_item_id"]
            meal_item.invoice_line_item_id=invoice_line_item_id
 
        if 'meal_id' in kwargs:
            meal_item.invoice_id=kwargs["meal_id"]
        if 'discount_percentage' in kwargs:
            meal_item.discount_percentage=kwargs["discount_percentage"]
        if 'quantity' in kwargs:
            meal_item.quantity=kwargs["quantity"]
        if 'unit_price' in kwargs:
            meal_item.unit_price=kwargs["unit_price"]
        if 'unit_name' in kwargs:
            meal_item.unit_name=kwargs["unit_name"]
        
        
        if 'save' in kwargs:
            save=kwargs["save"]
            if save:
                if 'coef' in kwargs:
                    coef=kwargs["coef"]
                    unit_name=kwargs["unit_name"]
                    unit_price=kwargs["unit_price"]
                if 'default' in kwargs:
                    default11=kwargs["default"]
                InvoiceLineItemUnitRepo(request=self.request).add_invoice_line_item_unit(
                    invoice_line_item_id=invoice_line_item_id,
                    coef=coef,
                    default=default11,
                    unit_name=unit_name,
                    unit_price=unit_price,
                    )

        result=SUCCEED
        message="آیتم وعده با موفقیت اضافه شد."     
 
        meal_item.save()
        return result,message,meal_item
