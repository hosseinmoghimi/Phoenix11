from django.db import models
from core.models import Page,LinkHelper,FAILED,SUCCEED
from django.utils.translation import gettext as _
from .apps import APP_NAME
# Create your models here.
class Project(Page,LinkHelper):

    

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
        message="آیتم غذایی با موفقیت اضافه شد."
        return (result,message,project)