from django.db import models
from core.models import _,reverse,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from phoenix.server_settings import CURRENCY
from .apps import APP_NAME
from accounting.models import Product,InvoiceLine,Invoice

class Food(models.Model,LinkHelper):
    name=models.CharField(_("نام"), max_length=50)
    items=models.ManyToManyField("fooditem", verbose_name=_("food items"))
    

    app_name=APP_NAME
    class_name="food"
    class Meta:
        verbose_name = _("Food")
        verbose_name_plural = _("Foods")

    def __str__(self):
        return self.name
 


class FoodItem(Product,LinkHelper):
    
    app_name=APP_NAME
    class_name="fooditem"

    class Meta:
        verbose_name = _("FoodItem")
        verbose_name_plural = _("FoodItems")
 
   
    def save(self):
        (result,message,food_item)=FAILED,'',self
        if self.class_name is None or self.class_name=="":
            self.class_name="fooditem"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(FoodItem,self).save()
        result=SUCCEED
        message="آیتم غذایی با موفقیت اضافه شد."
        return (result,message,food_item)

class Meal(Invoice):
     
    class Meta:
        verbose_name = _("Meal")
        verbose_name_plural = _("Meals")
 
   

    def save(self):
        (result,message,meal)=FAILED,"",None
        if self.class_name is None or self.class_name=="":
            self.class_name="meal"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(Meal,self).save()
        meal=self
        result=SUCCEED
        message="با موفقیت ذخیره شد."
        return (result,message,meal)
    

class MealItem(InvoiceLine,LinkHelper):
    app_name=APP_NAME
    class_name="mealitem"
    class Meta:
        verbose_name = _("MealItem")
        verbose_name_plural = _("MealItems")

    def __str__(self):
        return f'{self.meal} :  {self.invoice_line_item} * {self.quantity} $ {self.unit_price} {CURRENCY}'
 
    @property
    def meal(self):
        return Meal.objects.filter(pk=self.invoice.id).first()
    @property
    def food_item(self):
        return FoodItem.objects.filter(pk=self.invoice_line_item.id).first()