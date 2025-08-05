from django.db import models
from core.models import _,reverse,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from phoenix.server_settings import CURRENCY
from .apps import APP_NAME
from accounting.models import Product 
 

class Drug(Product,LinkHelper):
    
    app_name=APP_NAME
    class_name="drug"

    class Meta:
        verbose_name = _("Drug")
        verbose_name_plural = _("Drugs")
 
   
    def save(self):
        (result,message,drug)=FAILED,'',self
        if self.class_name is None or self.class_name=="":
            self.class_name="drug"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(Drug,self).save()
        result=SUCCEED
        message="دارو با موفقیت اضافه شد."
        return (result,message,drug)
 