from django.db import models
from utility.models import _,LinkHelper,DateTimeHelper
from accounting.models import UnitNameEnum,CorePage,FAILED,SUCCEED
from .apps import APP_NAME
from accounting.models import Asset


 
class Vehicle(Asset):
    class_name="vehicle"
    class Meta:
        verbose_name = _("Vehicle")
        verbose_name_plural = _("Vehicles")
  
    def save(self):
        (result,message,vehicle)=FAILED,'',self
        if self.class_name is None or self.class_name=="":
            self.class_name="vehicle"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(Vehicle,self).save()   
        result=SUCCEED
        message="وسیله نقلیه با موفقیت اضافه شد."
        return (result,message,vehicle)
         
  