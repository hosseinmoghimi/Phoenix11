from django.db import models
from core.models import _,reverse,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from phoenix.server_settings import CURRENCY
from .apps import APP_NAME
from accounting.models import Product,InvoiceLine,Invoice,CorePage
from .enums import *
from utility.enums import *
from projectmanager.models import Request


class WareHouse(models.Model,LinkHelper):
    name=models.CharField(_("نام"), max_length=50)
    account=models.ForeignKey("accounting.account", verbose_name=_("account"),null=True,blank=True, on_delete=models.PROTECT)
    organization_unit=models.ForeignKey("organization.organizationunit", verbose_name=_("organization_unit"),null=True,blank=True, on_delete=models.PROTECT)

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
 
 

class MaterialPort(models.Model,LinkHelper,DateTimeHelper):
    person=models.ForeignKey("authentication.person", verbose_name=_("person"), on_delete=models.CASCADE)
    source=models.ForeignKey("warehouse",related_name="material_from", verbose_name=_("source"), on_delete=models.PROTECT)
    destination=models.ForeignKey("warehouse",related_name="material_to", verbose_name=_("destination"), on_delete=models.PROTECT)
    product=models.ForeignKey("accounting.product", verbose_name=_("product"), on_delete=models.CASCADE)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    quantity=models.IntegerField(_("quantity"),default=1)
    unit_name=models.CharField(_("unit_name"),choices=UnitNameEnum.choices,default=UnitNameEnum.ADAD,max_length=100)
    direction=models.CharField(_("direction"),max_length=50,choices=MaterialPortDirectionEnum.choices)
    class_name="materialport"
    app_name=APP_NAME

    class Meta:
        verbose_name = _("MaterialPort")
        verbose_name_plural = _("MaterialPorts")

    def __str__(self):
        return f"{self.profile}  {self.product}  {self.direction}"


class WareHouseMaterialSheet(models.Model,LinkHelper):
    ware_house=models.ForeignKey("warehouse", verbose_name=_("ware_house"), on_delete=models.PROTECT)
    material=models.ForeignKey("accounting.product", verbose_name=_("product"), on_delete=models.PROTECT)
    direction=models.CharField(_("direction"),max_length=50,choices=MaterialPortDirectionEnum.choices)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    person=models.ForeignKey("authentication.person", verbose_name=_("person"), on_delete=models.PROTECT)
    unit_name=models.CharField(_("unit_name"),choices=UnitNameEnum.choices,default=UnitNameEnum.ADAD,max_length=100)
    quantity=models.IntegerField(_("quantity"))
    shelf=models.CharField(_("shelf"),max_length=50)
    row=models.CharField(_("row"),max_length=50)
    col=models.CharField(_("col"),max_length=50)

    class_name="warehousematerialsheet"
    app_name=APP_NAME
    class Meta:
        verbose_name = _("WareHouseMaterialSheet")
        verbose_name_plural = _("WareHouseMaterialSheets")

    def __str__(self):
        return f"{self.ware_house} - {self.material} - {self.direction}     "

    def balance(self):
        if self.direction==MaterialPortDirectionEnum.IN:
            return self.quantity
        if self.direction==MaterialPortDirectionEnum.OUT:
            return 0-self.quantity


class MaterialTerminal(models.Model):
    employee=models.ForeignKey("organization.employee",null=True,blank=True, verbose_name=_("employee"), on_delete=models.CASCADE)
    ware_house=models.ForeignKey("warehouse",null=True,blank=True, verbose_name=_("warehouse"), on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = _("MaterialTerminal")
        verbose_name_plural = _("MaterialTerminals")

    def __str__(self):
        employee=ware_house=''
        if self.employee is not None:
            employee= f"{self.employee}"
        if self.ware_house is not None:
            ware_house= f"{str(self.ware_house)}"
        return ware_house+"___"+employee