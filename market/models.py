from django.db import models
from utility.models import _,LinkHelper,DateTimeHelper
from accounting.models import UnitNameEnum,CorePage,FAILED,SUCCEED
from .apps import APP_NAME




class MarketPerson(models.Model,LinkHelper):
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"),null=True,blank=True, on_delete=models.SET_NULL)

    app_name=APP_NAME
    class Meta:
        verbose_name = _("MarketPerson")
        verbose_name_plural = _("MarketPersons")

    def __str__(self):
        return self.profile.full_name



class Customer(MarketPerson):
    class_name="customer"
    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
 
 
class Supplier(MarketPerson):

    class_name="supplier"
    class Meta:
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")
 
 
class Shipper(MarketPerson):
    class_name="shipper"

    class Meta:
        verbose_name = _("Shipper")
        verbose_name_plural = _("Shippers")
 
 

class Shop(models.Model,LinkHelper,DateTimeHelper):
    supplier=models.ForeignKey("supplier", verbose_name=_("supplier"), on_delete=models.CASCADE)
    product=models.ForeignKey("accounting.product", verbose_name=_("product"), on_delete=models.CASCADE)
    unit_name=models.CharField(_("unit_name"),choices=UnitNameEnum.choices, max_length=50)
    unit_price=models.IntegerField(_("قیمت واحد"))
    discount_percentage=models.IntegerField(_("درصد تخفیف"),default=0)
    quantity=models.IntegerField(_("quantity"))
    available=models.IntegerField(_("available"))
    date_added=models.DateTimeField(_("تاریخ ثبت "), auto_now=False, auto_now_add=True)
    start_date=models.DateTimeField(_("تاریخ شروع "), auto_now=False, auto_now_add=False)
    end_date=models.DateTimeField(_("تاریخ پایان "), auto_now=False, auto_now_add=False)
    app_name=APP_NAME
    class_name="shop"

    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")

    def __str__(self):
        return f'{self.product} @ {self.supplier} $ {self.unit_name} {self.unit_price}'
 


class CartItem(models.Model):
    row=models.IntegerField(_("ردیف"),default=1,blank=True)
    customer=models.ForeignKey("customer", verbose_name=_("مشتری"), on_delete=models.CASCADE)
    shop=models.ForeignKey("shop", verbose_name=_("فروش"), on_delete=models.CASCADE)
    quantity=models.IntegerField(_("تعداد"),default=1)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    description=models.CharField(_("توضیحات"),null=True,blank=True, max_length=50)

    class Meta:
        verbose_name = _("CartItem")
        verbose_name_plural = _("CartItems")

    def __str__(self):
        return f"{self.customer} @ {self.shop} # {self.quantity} {self.shop.unit_name}"
 
class Menu(CorePage):
    supplier=models.ForeignKey("supplier", verbose_name=_("supplier"), on_delete=models.CASCADE)
    # title=models.CharField(_("title"), max_length=50)
    shops=models.ManyToManyField("shop", verbose_name=_("shops"),blank=True)
    

    class Meta:
        verbose_name = _("Menu")
        verbose_name_plural = _("Menus")
    def save(self):
        (result,message,menu)=FAILED,'',self
        if self.class_name is None or self.class_name=="":
            self.class_name="menu"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(Menu,self).save()   
        result=SUCCEED
        message="آیتم غذایی با موفقیت اضافه شد."
        return (result,message,menu)
         
 