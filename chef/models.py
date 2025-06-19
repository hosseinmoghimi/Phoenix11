from django.db import models
from core.models import _,reverse,Page,LinkHelper,DateTimeHelper
from phoenix.server_settings import CURRENCY
from .apps import APP_NAME
class Food(models.Model,LinkHelper):
    name=models.CharField(_("نام"), max_length=50)
    items=models.ManyToManyField("fooditem", verbose_name=_("food items"))
    

    app_name=APP_NAME
    class_name="food    "
    class Meta:
        verbose_name = _("Food")
        verbose_name_plural = _("Foods")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Food_detail", kwargs={"pk": self.pk})



class FoodItem(models.Model,LinkHelper):
    name=models.CharField(_("نام"), max_length=50)
    price=models.IntegerField(_("قیمت"))
    
    app_name=APP_NAME
    class_name="fooditem"

    class Meta:
        verbose_name = _("FoodItem")
        verbose_name_plural = _("FoodItems")

    def __str__(self):
        return self.name
  

class Meal(models.Model,DateTimeHelper,LinkHelper):
    name=models.CharField(_("نام"), max_length=50)
    datetime=models.DateTimeField(_("تاریخ"), auto_now=False, auto_now_add=False)
    app_name=APP_NAME
    class_name="meal"
    class Meta:
        verbose_name = _("Meal")
        verbose_name_plural = _("Meals")

    def __str__(self):
        return f"{self.name}  {self.datetime}"
 

class MealItem(models.Model,LinkHelper):
    meal=models.ForeignKey("meal", verbose_name=_("meal"), on_delete=models.CASCADE)
    food_item=models.ForeignKey("fooditem", verbose_name=_("fooditem"), on_delete=models.CASCADE)
    quantity=models.IntegerField(_("quantity"))
    price=models.IntegerField(_("price"))
    app_name=APP_NAME
    class_name="mealitem"
    class Meta:
        verbose_name = _("MealItem")
        verbose_name_plural = _("MealItems")

    def __str__(self):
        return f'{self.meal} :  {self.food_item} * {self.quantity} $ {self.price} {CURRENCY}'
 