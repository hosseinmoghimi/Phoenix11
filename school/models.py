from django.db import models
from core.models import _,reverse,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from phoenix.server_settings import CURRENCY
from .apps import APP_NAME
from accounting.models import Product,InvoiceLine,Invoice

class School(models.Model,LinkHelper):
    name=models.CharField(_("نام"), max_length=50)
     

    app_name=APP_NAME
    class_name="school"
    class Meta:
        verbose_name = _("School")
        verbose_name_plural = _("Schools")

    def __str__(self):
        return self.name
 

 
class CourseClass(models.Model,LinkHelper):
    name=models.CharField(_("نام"), max_length=50)
     

    app_name=APP_NAME
    class_name="courseclass"
    class Meta:
        verbose_name = _("CourseClass")
        verbose_name_plural = _("CourseClasses")

    def __str__(self):
        return self.name
 

 
class Course(models.Model,LinkHelper):
    name=models.CharField(_("نام"), max_length=50)
     

    app_name=APP_NAME
    class_name="course"
    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def __str__(self):
        return self.name
 
  