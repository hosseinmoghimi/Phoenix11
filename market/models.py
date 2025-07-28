from django.db import models
from utility.models import _,LinkHelper,DateTimeHelper
from accounting.models import UnitNameEnum,CorePage,FAILED,SUCCEED
from .apps import APP_NAME
from .enums import *



class MarketPerson(models.Model,LinkHelper):
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)
    person=models.ForeignKey("authentication.person",verbose_name=_("person"), on_delete=models.PROTECT)

    app_name=APP_NAME
    class Meta:
        verbose_name = _("MarketPerson")
        verbose_name_plural = _("MarketPersons")

    def __str__(self):
        return f'{self.account} # {self.person.full_name}'
    
    def full_name(self):
        return self.person.full_name

class Customer(MarketPerson):

    level=models.CharField(_("level"),choices=ShopLevelEnum.choices,default=ShopLevelEnum.END_USER, max_length=50)

    class_name="customer"
    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
 
 
    def save(self,*args, **kwargs):
        result,message,customer=FAILED,'',self
        super(Customer,self).save()
        return result,message,customer
    
     
    
class Supplier(MarketPerson):
    level=models.CharField(_("level"),choices=ShopLevelEnum.choices,default=ShopLevelEnum.END_USER, max_length=50)

    class_name="supplier"
    class Meta:
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")
 
    def save(self,*args, **kwargs):
        result,message,supplier=FAILED,'',self

        super(Supplier,self).save()
        result=SUCCEED
        message='فروشنده اضافه شد.'
        return result,message,supplier


class Shipper(MarketPerson):
    class_name="shipper"

    class Meta:
        verbose_name = _("Shipper")
        verbose_name_plural = _("Shippers")
 
 
    def save(self,*args, **kwargs):
        result,message,shipper=FAILED,'',self
        super(Shipper,self).save()
        return result,message,shipper

class ShopPackage(models.Model,LinkHelper,DateTimeHelper):
    supplier=models.ForeignKey("supplier", verbose_name=_("supplier"), on_delete=models.CASCADE)
    title=models.CharField(_("title"), max_length=50)    
    shops=models.ManyToManyField("shop", verbose_name=_("shops"))
    level=models.CharField(_("level"),choices=ShopLevelEnum.choices,default=ShopLevelEnum.END_USER, max_length=50)
    start_date=models.DateTimeField(_("تاریخ شروع "), auto_now=False, auto_now_add=False)
    end_date=models.DateTimeField(_("تاریخ پایان "), auto_now=False, auto_now_add=False)
    quantity=models.IntegerField(_("تعداد کل"))
    available=models.IntegerField(_("موجود"))


    class_name='shoppackage'
    app_name=APP_NAME
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = _("ShopPackage")
        verbose_name_plural = _("ShopPackages")

    def save(self):
        (result,message,shop_package)=FAILED,'',self
        if self.class_name is None or self.class_name=="":
            self.class_name="shop_package"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(ShopPackage,self).save()   
        result=SUCCEED
        message="پکیج با موفقیت اضافه شد."
        return (result,message,shop_package)

class Shop(models.Model,LinkHelper,DateTimeHelper):
    supplier=models.ForeignKey("supplier", verbose_name=_("supplier"), on_delete=models.CASCADE)
    product=models.ForeignKey("accounting.product", verbose_name=_("product"), on_delete=models.CASCADE)
    level=models.CharField(_("level"),choices=ShopLevelEnum.choices,default=ShopLevelEnum.END_USER, max_length=50)
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
         
 
class Desk(models.Model,LinkHelper):
    title=models.CharField(_("title"), max_length=50)
    code=models.CharField(_("code"),null=True,blank=True, max_length=50)
    supplier=models.ForeignKey("supplier", verbose_name=_("supplier"), on_delete=models.CASCADE)
    app_name=APP_NAME
    class_name='desk'


    class Meta:
        verbose_name = _("Desk")
        verbose_name_plural = _("Desks")
    def __str__(self):
        return self.title
    def save(self):
        (result,message,desk)=FAILED,'',self
         
        super(Desk,self).save()   
        result=SUCCEED
        message="میز با موفقیت اضافه شد."
        return (result,message,desk)


class DeskCustomer(Customer):
    desk=models.ForeignKey("desk", verbose_name=_("desk"), on_delete=models.CASCADE)
    class_name="deskcustomer"

    class Meta:
        verbose_name = _("DeskCustomer")
        verbose_name_plural = _("DeskCustomers")  

 








