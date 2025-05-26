from django.db import models
from utility.models import _,LinkHelper
from accounting.models import UnitNameEnum

class MarketPerson(models.Model,LinkHelper):
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"),null=True,blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("MarketPerson")
        verbose_name_plural = _("MarketPersons")

    def __str__(self):
        return self.profile.full_name
 


class Customer(MarketPerson):

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
 
 
class Supplier(MarketPerson):

    class Meta:
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")
 
 
class Shipper(MarketPerson):

    class Meta:
        verbose_name = _("Shipper")
        verbose_name_plural = _("Shippers")
 
 

class Shop(models.Model,LinkHelper):
    supplier=models.ForeignKey("supplier", verbose_name=_("supplier"), on_delete=models.CASCADE)
    product=models.ForeignKey("accounting.product", verbose_name=_("product"), on_delete=models.CASCADE)
    unit_name=models.CharField(_("unit_name"),choices=UnitNameEnum.choices, max_length=50)
    unit_price=models.IntegerField(_("قیمت واحد"))
    date_added=models.DateTimeField(_("تاریخ ثبت "), auto_now=False, auto_now_add=True)
    date_start=models.DateTimeField(_("تاریخ شروع "), auto_now=False, auto_now_add=False)
    date_end=models.DateTimeField(_("تاریخ پایان "), auto_now=False, auto_now_add=False)
    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")

    def __str__(self):
        return f'{self.unit_price}'
 