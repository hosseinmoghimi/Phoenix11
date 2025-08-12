from django.db import models
from core.models import _,reverse,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from phoenix.server_settings import CURRENCY
from .apps import APP_NAME
from accounting.models import FinancialEvent


class Tax(FinancialEvent):

    app_name=APP_NAME
    class_name="tax"
    class Meta:
        verbose_name = _("Tax")
        verbose_name_plural = _("Taxs")
 

    def save(self):
         (result,message,tax)=FAILED,'',self
         super(Tax,self).save()
         result=SUCCEED
         message='مالیات با موفقیت اضافه شد.'
         return  (result,message,tax)
 