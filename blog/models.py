from django.db import models
from core.models import _,reverse,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from phoenix.server_settings import CURRENCY
from .apps import APP_NAME
from accounting.models import FinancialEvent

class Blog(Page):

    
    app_name=APP_NAME
    class_name="blog"

    class Meta:
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")
 
 

    def save(self):
         if self.class_name is None or self.class_name=='':
             self.class_name='blog'
         if self.app_name is None or self.app_name=='':
             self.app_name=APP_NAME

         (result,message,blog)=FAILED,'',self
         super(Blog,self).save()
         result=SUCCEED
         message='بلاگ با موفقیت ذخیره شد.'
         return  (result,message,blog)
 