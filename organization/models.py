from django.db import models
from core.models import Page,LinkHelper,FAILED,SUCCEED
from django.utils.translation import gettext as _
from .apps import APP_NAME
# Create your models here.
class Organization(Page,LinkHelper):

    

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")
 
    def save(self):
        (result,message,organization)=FAILED,'',self
        if self.class_name is None or self.class_name=="":
            self.class_name="organization"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(Organization,self).save()
        result=SUCCEED
        message="سازمان با موفقیت اضافه شد."
        return (result,message,organization)