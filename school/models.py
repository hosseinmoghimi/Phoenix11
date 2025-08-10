from django.db import models
from core.models import _,reverse,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from phoenix.server_settings import CURRENCY
from .apps import APP_NAME
from accounting.models import Product,InvoiceLine,Invoice,CorePage

class School(models.Model,LinkHelper):
    name=models.CharField(_("نام"), max_length=50)
    person_account=models.ForeignKey("accounting.personaccount", verbose_name=_("person_account"), on_delete=models.CASCADE)

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

 
class Course(CorePage,LinkHelper):
 
    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
 
    
    def save(self):
        (result,message,course)=FAILED,'',self
        if self.class_name is None or self.class_name=="":
            self.class_name='course'
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(Course,self).save()
        result=SUCCEED
        message='واحد درسی با موفقیت اضافه شد.'
        return (result,message,course)
 
  
class CourseClass(models.Model,LinkHelper):
    school=models.ForeignKey("school", verbose_name=_("school"), on_delete=models.CASCADE) 
    course=models.ForeignKey("course", verbose_name=_("course"), on_delete=models.CASCADE) 
    room=models.CharField(_("room"), max_length=50)
    teachers=models.ManyToManyField("teacher", verbose_name=_("teachers"))
    students=models.ManyToManyField("student", verbose_name=_("students"))
    app_name=APP_NAME
    class_name="courseclass"
    class Meta:
        verbose_name = _("CourseClass")
        verbose_name_plural = _("CourseClasses")

    def __str__(self):
        return f"{self.school} : {self.course} @ {self.room} " 
 

class Student(models.Model,LinkHelper):
    person=models.ForeignKey("authentication.person", verbose_name=_("person"), on_delete=models.CASCADE)
    
    class_name="student"
    app_name=APP_NAME
    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")

    def __str__(self):
        return self.person.full_name
 

class Teacher(models.Model,LinkHelper):
    person=models.ForeignKey("authentication.person", verbose_name=_("person"), on_delete=models.CASCADE)
    
    class_name="teacher"
    app_name=APP_NAME
    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")

    def __str__(self):
        return self.person.full_name 