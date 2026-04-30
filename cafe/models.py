from django.db import models
from core.models import _,reverse,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from phoenix.server_settings import CURRENCY
from .apps import APP_NAME
from accounting.models import Product,InvoiceLine,Invoice

class Table(models.Model,LinkHelper):
    class_name="table"
    app_name=APP_NAME
    title=models.CharField(_("عنوان"), max_length=50)
    table_no=models.IntegerField(_("شماره میز"), default=0)
    

    class Meta:
        verbose_name = _("Table")
        verbose_name_plural = _("Tables")

    def __str__(self):
        return self.title
   
    class Meta:
        verbose_name = _("MealItem")
        verbose_name_plural = _("MealItems")
 