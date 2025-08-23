from django.db import models
from core.models import _,reverse,Event,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from phoenix.server_settings import CURRENCY
from .apps import APP_NAME 

class Appointment(Event):
    person_to_meet=models.ForeignKey("authentication.person", verbose_name=_("person"), on_delete=models.CASCADE)
    
    app_name=APP_NAME
    class_name="appointment"

    class Meta:
        verbose_name = _("Appointment")
        verbose_name_plural = _("Appointmentes")
 

    def save(self):
        if self.class_name is None or self.class_name=='':
            self.class_name='appointment'
        if self.app_name is None or self.app_name=='':
            self.app_name=APP_NAME
        (result,message,appointment)=FAILED,'',self
        super(Appointment,self).save()
        result=SUCCEED
        message='قرار ملاقات با موفقیت اضافه شد.'
        return  (result,message,appointment)
 