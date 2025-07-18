from django.db import models
from core.models import Page,LinkHelper,FAILED,SUCCEED
from django.utils.translation import gettext as _
from .apps import APP_NAME
from utility.models import DateTimeHelper
# Create your models here.
class OrganizationUnit(Page,LinkHelper):
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = _("OrganizationUnit")
        verbose_name_plural = _("OrganizationUnits")
 
    def save(self):
        (result,message,organization_unit)=FAILED,'',self
        if self.class_name is None or self.class_name=="":
            self.class_name="organizationunit"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(OrganizationUnit,self).save()
        result=SUCCEED
        message="سازمان با موفقیت اضافه شد."
        return (result,message,organization_unit)
    


    
class Employee(models.Model,LinkHelper,DateTimeHelper):
    person=models.ForeignKey("authentication.person",related_name="employees", verbose_name=_("person"), on_delete=models.CASCADE)
    organization_unit=models.ForeignKey("organizationunit",null=True,blank=True, verbose_name=_("parent"), on_delete=models.CASCADE)
    job_title=models.CharField(_("job_title"),max_length=100)

    class_name="employee"
    app_name=APP_NAME

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")

    def __str__(self):
        return f"{self.person}  {self.job_title}  {self.organization_unit}"
 
 
    def save(self):
        (result,message,employee)=FAILED,'',self
        super(Employee,self).save()
        result=SUCCEED
        message='کارمند جدید با موفقیت اضافه شد.'
        return (result,message,employee)