from django.db import models
from core.models import _,reverse,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from phoenix.server_settings import CURRENCY
from .apps import APP_NAME
from accounting.models import FinancialEvent

class SampleClass(models.Model):

    
    app_name=APP_NAME
    class_name="sampleclass"

    class Meta:
        verbose_name = _("SampleClass")
        verbose_name_plural = _("SampleClasses")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("SampleClass_detail", kwargs={"pk": self.pk})
  

    def save(self):
        (result,message,sample_class)=FAILED,'',self
        super(SampleClass,self).save()
        result=SUCCEED
        message='کلاس نمونه با موفقیت اضافه شد.'
        return  (result,message,sample_class)
 