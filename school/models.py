from django.db import models
from core.models import _,reverse,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from phoenix.server_settings import CURRENCY
from .apps import APP_NAME
from accounting.models import Product,InvoiceLine,Invoice,CorePage
from utility.num import to_tartib
from .enums import *



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


class Major(models.Model,LinkHelper):
    title=models.CharField(_("title"), max_length=50)
    courses=models.ManyToManyField("course",blank=True, verbose_name=_("واحد های درسی"))   

    app_name=APP_NAME
    class_name='major'

    class Meta:
        verbose_name = _("Major")
        verbose_name_plural = _("Majors")

   
    def __str__(self):
        return self.title
    def save(self):
        (result,message,major)=FAILED,'',self
        if self.class_name is None or self.class_name=="":
            self.class_name='major'
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(Major,self).save()
        result=SUCCEED
        message='رشته درسی با موفقیت اضافه شد.'
        return (result,message,major)
 

  
 
class Course(CorePage,LinkHelper):
    # major=models.ForeignKey("major", verbose_name=_("رشته"), on_delete=models.CASCADE) 
    books=models.ManyToManyField("library.book",blank=True, verbose_name=_("books"))
    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("واحد های درسی")
 
    def __str__(self):
        return  f'{self.title} '
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
    major=models.ForeignKey("major", verbose_name=_("major"), on_delete=models.CASCADE) 
    level=models.IntegerField(_("پایه"))
    room=models.CharField(_("room"),null=True,blank=True, max_length=50)
    teachers=models.ManyToManyField("teacher",blank=True, verbose_name=_("teachers"))
    students=models.ManyToManyField("student",blank=True, verbose_name=_("students"))
    app_name=APP_NAME
    class_name="courseclass"
    class Meta:
        verbose_name = _("CourseClass")
        verbose_name_plural = _("واحد های درسی جاری")

    def __str__(self):
        return f"{self.school} : {self.course} @ {self.room} @ {to_tartib(self.level)} {self.major} " 
 

class Student(models.Model,LinkHelper):
    person_account=models.ForeignKey("accounting.personaccount", verbose_name=_("person_account"), on_delete=models.PROTECT)
    
    class_name="student"
    app_name=APP_NAME
    class Meta:
        verbose_name = _("دانش آموز")
        verbose_name_plural = _("دانش آموزان")

    def __str__(self):
        return self.person_account.person.full_name 

    def save(self,*args, **kwargs):
        result=FAILED
        message=''
        student=None

        super(Student,self).save()
        student=self
        message='دانش آموز ذخیره شد.'
        result=SUCCEED
        return result,message,student

class Teacher(models.Model,LinkHelper):
    person_account=models.ForeignKey("accounting.personaccount", verbose_name=_("person_account"), on_delete=models.PROTECT)
    
    class_name="teacher"
    app_name=APP_NAME
    class Meta:
        verbose_name = _("مربی")
        verbose_name_plural = _("مربی ها")

    def __str__(self):
        return self.person_account.person.full_name 
    def save(self,*args, **kwargs):
        result=FAILED
        message=''
        teacher=None

        super(Teacher,self).save()
        teacher=self
        message='دبیر ذخیره شد.'
        result=SUCCEED
        return result,message,teacher