from django.db import models
from core.models import Event,LinkHelper,FAILED,SUCCEED
from .enums import *
from django.utils.translation import gettext as _
from .apps import APP_NAME
from accounting.models import InvoiceLine,Invoice
# Create your models here.
class Project(Event,LinkHelper): 
    employer=models.ForeignKey("organization.organization", verbose_name=_("employer"),related_name="project_employed", on_delete=models.CASCADE)
    contractor=models.ForeignKey("organization.organization", verbose_name=_("contractor"),related_name="project_contracted", on_delete=models.CASCADE)
    type=models.CharField(_("تایپ"),max_length=50,choices=ProjectTypeEnum.choices,default=ProjectTypeEnum.TYPE_A)
    percentage_completed=models.IntegerField(_("درصد پیشرفت"),default=0)
    weight=models.IntegerField(_("وزن پروژه"),default=0)
    invoices=models.ManyToManyField("accounting.invoice", verbose_name=_("invoices"))
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

 
 
















