from django.db import models
from core.models import _,reverse,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from phoenix.server_settings import CURRENCY
from .apps import APP_NAME
from accounting.models import Product,InvoiceLine,Invoice,CorePage

class School(models.Model,LinkHelper):
    name=models.CharField(_("نام"), max_length=50)
    account=models.ForeignKey("accounting.account", verbose_name=_("account"),null=True,blank=True, on_delete=models.CASCADE)

    app_name=APP_NAME
    class_name="school"
    class Meta:
        verbose_name = _("School")
        verbose_name_plural = _("Schools")

    def __str__(self):
        return self.name
 

    def save(self):
         (result,message,school)=FAILED,'',self
         super(School,self).save()
         result=SUCCEED
         message='آموزشگاه با موفقیت اضافه شد.'
         return  (result,message,school)
class CourseClass(models.Model,LinkHelper):
    course=models.ForeignKey("course", verbose_name=_("course"), on_delete=models.CASCADE) 
    school=models.ForeignKey("school", verbose_name=_("school"), on_delete=models.CASCADE) 

    app_name=APP_NAME
    class_name="courseclass"
    class Meta:
        verbose_name = _("CourseClass")
        verbose_name_plural = _("CourseClasses")

    def __str__(self):
        return self.name
 

 
class Course(CorePage,LinkHelper):
    name=models.CharField(_("نام"), max_length=50)
     
 
    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
 
  
    def save(self):
        if self.class_name is None or self.class_name=="":
            self.class_name='course'
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(Course,self).save()
 
  