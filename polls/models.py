from django.db import models
from core.models import _,reverse,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from phoenix.server_settings import CURRENCY
from .apps import APP_NAME
from accounting.models import FinancialEvent

class Poll(Page):
    
    app_name=APP_NAME
    class_name="poll"

    class Meta:
        verbose_name = _("Poll")
        verbose_name_plural = _("Polles")

 

    def save(self):
        if self.class_name is None or self.class_name=='':
            self.class_name='poll'
        if self.app_name is None or self.app_name=='':
            self.app_name=APP_NAME
        (result,message,poll)=FAILED,'',self
        super(Poll,self).save()
        result=SUCCEED
        message='کلاس نمونه با موفقیت اضافه شد.'
        return  (result,message,poll)
 