from django.db import models
from core.models import _,reverse,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from phoenix.server_settings import CURRENCY
from .apps import APP_NAME
from accounting.models import Product,InvoiceLine,Invoice,CorePage

class WareHouse(models.Model,LinkHelper):
    name=models.CharField(_("نام"), max_length=50)
    account=models.ForeignKey("accounting.account", verbose_name=_("account"),null=True,blank=True, on_delete=models.CASCADE)

    app_name=APP_NAME
    class_name="warehouse"
    class Meta:
        verbose_name = _("WareHouse")
        verbose_name_plural = _("WareHouses")

    def __str__(self):
        return self.name
 

    def save(self):
         (result,message,warehouse)=FAILED,'',self
         super(WareHouse,self).save()
         result=SUCCEED
         message='انبار با موفقیت اضافه شد.'
         return  (result,message,warehouse)
 