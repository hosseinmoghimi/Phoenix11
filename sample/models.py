from django.db import models
from core.models import _,reverse,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from phoenix.server_settings import CURRENCY
from .apps import APP_NAME
from accounting.models import FinancialEvent

class Sample(models.Model):

    
    app_name=APP_NAME
    class_name="sample"

    class Meta:
        verbose_name = _("Sample")
        verbose_name_plural = _("Samples")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Sample_detail", kwargs={"pk": self.pk})
  

    def save(self):
         (result,message,sample)=FAILED,'',self
         super(Sample,self).save()
         result=SUCCEED
         message='مالیات با موفقیت اضافه شد.'
         return  (result,message,sample)
 