from django.db import models
from utility.models import _,LinkHelper

class Shop(models.Model,LinkHelper):

    unit_price=models.IntegerField(_("قیمت واحد"))

    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")

    def __str__(self):
        return f'{self.unit_price}'
 