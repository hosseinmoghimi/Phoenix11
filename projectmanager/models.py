from django.db import models
from core.models import Event,LinkHelper,FAILED,SUCCEED
from .enums import *
from django.utils.translation import gettext as _
from .apps import APP_NAME
from accounting.models import InvoiceLine,Invoice
# Create your models here.
class Project(Event,LinkHelper): 
    employer=models.ForeignKey("organization.organizationunit", verbose_name=_("employer"),related_name="project_employed", on_delete=models.CASCADE)
    contractor=models.ForeignKey("organization.organizationunit", verbose_name=_("contractor"),related_name="project_contracted", on_delete=models.CASCADE)
    type=models.CharField(_("تایپ"),max_length=50,choices=ProjectTypeEnum.choices,default=ProjectTypeEnum.TYPE_A)
    percentage_completed=models.IntegerField(_("درصد پیشرفت"),default=0)
    weight=models.IntegerField(_("وزن پروژه"),default=0)
    invoices=models.ManyToManyField("accounting.invoice", verbose_name=_("invoices"))
    remote_clients=models.ManyToManyField("remoteclient", verbose_name=_("remote_clients"))
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
 
    def save(self):
        (result,message,project)=FAILED,'',self
        if self.class_name is None or self.class_name=="":
            self.class_name="project"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(Project,self).save()
        result=SUCCEED
        message="پروژه با موفقیت اضافه شد."
        return (result,message,project)
    

class Request(InvoiceLine):
    ware_house=models.ForeignKey("warehouse.warehouse", verbose_name=_("ware_house"), on_delete=models.PROTECT)

    

    class Meta:
        verbose_name = _("Request")
        verbose_name_plural = _("Requests")
    def save(self):
        super(Request,self).save()


class MaterialRequest(Request):
    

    class Meta:
        verbose_name = _("MaterialRequest")
        verbose_name_plural = _("MaterialRequests")
    def save(self):
        super(MaterialRequest,self).save()


class ServiceRequest(Request):
    

    class Meta:
        verbose_name = _("ServiceRequest")
        verbose_name_plural = _("ServiceRequests")
    def save(self):
        super(ServiceRequest,self).save()

 
 

class RemoteClient(models.Model,LinkHelper):
   
    name=models.CharField(_("name"), max_length=100)
    active_directory=models.CharField(_("active_directory"),null=True,blank=True, max_length=100)
    work_group=models.CharField(_("work_group"),null=True,blank=True, max_length=50)
    os=models.CharField(_("Operating System (os)"),null=True,blank=True, max_length=50)
    url=models.CharField(_("url"),null=True,blank=True, max_length=500)
    local_ip=models.CharField(_("local_ip"),null=True,blank=True, max_length=50)
    remote_ip=models.CharField(_("remote_ip"),null=True,blank=True, max_length=50)
    any_desk_address=models.CharField(_("any_desk_address"),null=True,blank=True, max_length=50)
    any_desk_password=models.CharField(_("any_desk_password"),null=True,blank=True, max_length=50)
    dorsan_desk_address=models.CharField(_("dorsan_desk_address"),null=True,blank=True, max_length=50)
    dorsan_desk_password=models.CharField(_("dorsan_desk_password"),null=True,blank=True, max_length=50)
    brand=models.ForeignKey("accounting.brand",null=True,blank=True, verbose_name=_("brand"), on_delete=models.SET_NULL)
    model_name=models.CharField(_("model name"),null=True,blank=True, max_length=50)
    id_name=models.CharField(_("id_name"),null=True,blank=True, max_length=50)
    mac_address=models.CharField(_("mac_address"),null=True,blank=True, max_length=50)
    serial_no=models.CharField(_("serial_no"),null=True,blank=True, max_length=50)
    part_no=models.CharField(_("part_no"),null=True,blank=True, max_length=50)
    username=models.CharField(_("username"),null=True,blank=True, max_length=50)
    password=models.CharField(_("password"),null=True,blank=True, max_length=50)
    identity=models.CharField(_("identity"),null=True,blank=True, max_length=50)
    wireless_mode=models.CharField(_("wireless_mode"),null=True,blank=True, max_length=50)
    wireless_band=models.CharField(_("wireless_band"),null=True,blank=True, max_length=50)
    ssid=models.CharField(_("ssid"),null=True,blank=True, max_length=50)
    preshared_key=models.CharField(_("preshared_key"),null=True,blank=True, max_length=50)
    frequency=models.CharField(_("frequency"),null=True,blank=True, max_length=50)
    protocol=models.CharField(_("protocol"),null=True,blank=True, max_length=50)
    channel_width=models.CharField(_("channel_width"),null=True,blank=True, max_length=50)
    adsl_username=models.CharField(_("adsl_username"),null=True,blank=True, max_length=50)
    adsl_password=models.CharField(_("adsl_password"),null=True,blank=True, max_length=50)
    telephone=models.CharField(_("telephone"),null=True,blank=True, max_length=50)
    contact=models.CharField(_("contact"),null=True,blank=True, max_length=50)
    description=models.TextField(_("description"),null=True,blank=True, max_length=2000)
    
    class_name="remoteclient"
    app_name=APP_NAME

    @property
    def get_project_absolute_url(self):
        project=self.project_set.first()
        if project is not None:
            return project.get_absolute_url()
   
    @property
    def get_project_title(self):
        project=self.project_set.first()
        if project is not None:
            return project.title
        
   
    class Meta:
        verbose_name = _("RemoteClient")
        verbose_name_plural = _("RemoteClients")

    def __str__(self):
        return self.name 

















