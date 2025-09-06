from django.db import models
from core.models import _,reverse,Event,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from phoenix.server_settings import CURRENCY
from .apps import APP_NAME 



class Task(Event):
    

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")




    def save(self):
        if self.class_name is None or self.class_name=='':
            self.class_name='task'
        if self.app_name is None or self.app_name=='':
            self.app_name=APP_NAME
        (result,message,appointment)=FAILED,'',self
        super(Task,self).save()
        result=SUCCEED
        message='تسک با موفقیت اضافه شد.'
        return  (result,message,appointment)
 
class Appointment(Task):
    persons_to_meet=models.ManyToManyField("authentication.person", verbose_name=_("person"))
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
 
