from django.db import models
from core.models import _,reverse,Page as CorePage,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from phoenix.server_settings import CURRENCY
from .apps import APP_NAME
from accounting.models import FinancialEvent

class Book(CorePage):

    
    app_name=APP_NAME
    class_name="sampleclass"

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Bookes")
 
 
    def save(self):
        if self.class_name is None or self.class_name =='':
            self.class_name="book"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        (result,message,sample_class)=FAILED,'',self
        super(Book,self).save()
        result=SUCCEED
        message='کلاس نمونه با موفقیت اضافه شد.'
        return  (result,message,sample_class)
 