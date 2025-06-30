from django.db import models
from core.models import Event,LinkHelper,FAILED,SUCCEED
from .enums import *
from django.utils.translation import gettext as _
from .apps import APP_NAME
# Create your models here.
class Project(Event,LinkHelper):
    employer=models.ForeignKey("organization.organization", verbose_name=_("employer"),related_name="project_employed", on_delete=models.CASCADE)
    contractor=models.ForeignKey("organization.organization", verbose_name=_("contractor"),related_name="project_contracted", on_delete=models.CASCADE)
    type=models.CharField(_("تایپ"),max_length=50,choices=ProjectTypeEnum.choices,default=ProjectTypeEnum.TYPE_A)
    percentage_completed=models.IntegerField(_("درصد پیشرفت"),default=0)
    weight=models.IntegerField(_("وزن پروژه"),default=0)
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