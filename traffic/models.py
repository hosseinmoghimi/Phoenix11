from django.db import models
from core.models import _,reverse,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from phoenix.server_settings import CURRENCY
from .apps import APP_NAME
from accounting.models import FinancialEvent

class Traffic(models.Model,DateTimeHelper,LinkHelper):
    person=models.ForeignKey("authentication.person", verbose_name=_("person"), on_delete=models.CASCADE)
    enter_datetime=models.DateTimeField(_("enter date time"), auto_now=False, auto_now_add=False)
    exit_datetime=models.DateTimeField(_("exit date time"), auto_now=False, auto_now_add=False)
    location=models.ForeignKey("attachments.location", verbose_name=_("location"), on_delete=models.CASCADE)
    app_name=APP_NAME
    class_name="traffic"

    class Meta:
        verbose_name = _("Traffic")
        verbose_name_plural = _("Traffics")

    def __str__(self):
        entity_name=''
        if self.person is not None:
            entity_name=self.person.full_name
        if self.person is not None:
            entity_name=self.person.full_name
        return f"{entity_name} {self.location}"
 

    def save(self):
        (result,message,traffic)=FAILED,'',self
        super(Traffic,self).save()
        result=SUCCEED
        message='کلاس نمونه با موفقیت اضافه شد.'
        return  (result,message,traffic)
 