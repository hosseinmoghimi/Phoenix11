from django.db import models
from core.models import _,reverse,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from phoenix.server_settings import CURRENCY
from .apps import APP_NAME
from accounting.models import FinancialEvent

class Family(models.Model,LinkHelper):
    father=models.ForeignKey("authentication.person", related_name='daddy_childs',verbose_name=_("father"), on_delete=models.CASCADE)
    mother=models.ForeignKey("authentication.person", related_name='mommy_childs',verbose_name=_("mother"), on_delete=models.CASCADE)
    childs=models.ManyToManyField("authentication.person", blank=True,verbose_name=_("childs"))    
    app_name=APP_NAME
    class_name="family"

    class Meta:
        verbose_name = _("Family")
        verbose_name_plural = _("Families")

    def __str__(self):
        return self.father.full_name
 

    def save(self):
        (result,message,family)=FAILED,'',self
        super(Family,self).save()
        result=SUCCEED
        message='کلاس نمونه با موفقیت اضافه شد.'
        return  (result,message,family)
 