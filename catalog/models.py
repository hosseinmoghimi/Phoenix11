from django.db import models
from core.models import _,reverse,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from phoenix.server_settings import CURRENCY
from .apps import APP_NAME
from utility.models import LinkHelper
from accounting.models import FinancialEvent

class Catalog(models.Model,LinkHelper):
    product=models.ForeignKey("accounting.product", verbose_name=_("product"), on_delete=models.CASCADE)
    title=models.CharField(_("title"), max_length=300)
    slogan=models.CharField(_("slogan"), max_length=600)

    app_name=APP_NAME
    class_name="catalog"

    class Meta:
        verbose_name = _("Catalog")
        verbose_name_plural = _("Cataloges")

    def __str__(self):
        return self.name
 
    def save(self):
        (result,message,catalog)=FAILED,'',self
        super(Catalog,self).save()
        result=SUCCEED
        message='کاتالوگ با موفقیت اضافه شد.'
        return  (result,message,catalog)
 