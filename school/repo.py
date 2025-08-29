from .models import School,Course,CourseClass,Teacher,Student,Major
from .apps import APP_NAME
from .enums import *
from log.repo import LogRepo 
from django.db.models import Q
from django.shortcuts import reverse
from authentication.repo import PersonRepo
from accounting.repo import InvoiceLineItemUnitRepo
from utility.num import filter_number
from utility.calendar import PersianCalendar
from utility.constants import FAILED,SUCCEED
from utility.log import leolog
from .enums import *


class SchoolRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=School.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=School.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def school(self,*args, **kwargs):
        if "school_id" in kwargs and kwargs["school_id"] is not None:
            return self.objects.filter(pk=kwargs['school_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_school(self,*args,**kwargs):
        result,message,school=FAILED,"",None
        if len(School.objects.filter(name=kwargs["name"]))>0:
            message='نام تکراری برای آموزشگاه جدید'
            return FAILED,message,None
        if len(School.objects.filter(person_account_id=kwargs["person_account_id"]))>0:
            message='حساب تکراری برای آموزشگاه جدید'
            return FAILED,message,None
        if not self.request.user.has_perm(APP_NAME+".add_school"):
            message="دسترسی غیر مجاز"
            return result,message,school

        school=School() 
        if 'person_account_id' in kwargs:
            school.person_account_id=kwargs["person_account_id"]
        if 'name' in kwargs:
            school.name=kwargs["name"]
          
        (result,message,school)=school.save()
        return result,message,school

 

class StudentRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Student.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=Student.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def student(self,*args, **kwargs):
        if "student_id" in kwargs and kwargs["student_id"] is not None:
            return self.objects.filter(pk=kwargs['student_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_student(self,*args,**kwargs):
        result,message,student=FAILED,"",None
        if len(Student.objects.filter(name=kwargs["name"]))>0:
            message='نام تکراری برای آموزشگاه جدید'
            return FAILED,message,None
        if len(Student.objects.filter(person_account_id=kwargs["person_account_id"]))>0:
            message='حساب تکراری برای آموزشگاه جدید'
            return FAILED,message,None
        if not self.request.user.has_perm(APP_NAME+".add_student"):
            message="دسترسی غیر مجاز"
            return result,message,student

        student=Student() 
        if 'person_account_id' in kwargs:
            student.person_account_id=kwargs["person_account_id"]
        if 'name' in kwargs:
            student.name=kwargs["name"]
          
        (result,message,student)=student.save()
        return result,message,student

 
 
class TeacherRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Teacher.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=Teacher.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def teacher(self,*args, **kwargs):
        if "teacher_id" in kwargs and kwargs["teacher_id"] is not None:
            return self.objects.filter(pk=kwargs['teacher_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_teacher(self,*args,**kwargs):
        result,message,teacher=FAILED,"",None
        if len(Teacher.objects.filter(person_account_id=kwargs["person_account_id"]))>0:
            message='نام تکراری برای آموزشگاه جدید'
            return FAILED,message,None
        if len(Teacher.objects.filter(person_account_id=kwargs["person_account_id"]))>0:
            message='حساب تکراری برای آموزشگاه جدید'
            return FAILED,message,None
        if not self.request.user.has_perm(APP_NAME+".add_teacher"):
            message="دسترسی غیر مجاز"
            return result,message,teacher

        teacher=Teacher() 
        if 'person_account_id' in kwargs:
            teacher.person_account_id=kwargs["person_account_id"]
        if 'name' in kwargs:
            teacher.name=kwargs["name"]
          
        (result,message,teacher)=teacher.save()
        return result,message,teacher

 


 
class MajorRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Major.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=Major.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def major(self,*args, **kwargs):
        if "major_id" in kwargs and kwargs["major_id"] is not None:
            return self.objects.filter(pk=kwargs['major_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_major(self,*args,**kwargs):
        result,message,major=FAILED,"",None
        if len(Major.objects.filter(title=kwargs["title"]))>0:
            message='نام تکراری برای رشته جدید'
            return FAILED,message,None
      
        if not self.request.user.has_perm(APP_NAME+".add_major"):
            message="دسترسی غیر مجاز"
            return result,message,major

        major=Major() 
        if 'title' in kwargs:
            major.title=kwargs["title"]
        
          
        (result,message,major)=major.save()
        return result,message,major

 
class CourseRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Course.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=Course.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def course(self,*args, **kwargs):
        if "course_id" in kwargs and kwargs["course_id"] is not None:
            return self.objects.filter(pk=kwargs['course_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_course(self,*args,**kwargs):
        result,message,course=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_course"):
            message="دسترسی غیر مجاز"
            return result,message,course

        course=Course()
        if 'title' in kwargs:
            course.title=kwargs["title"]
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                course.parent_id=kwargs["parent_id"]
        if 'color' in kwargs:
            course.color=kwargs["color"]
        if 'code' in kwargs:
            course.code=kwargs["code"]
        if 'priority' in kwargs:
            course.priority=kwargs["priority"]
        if 'type' in kwargs:
            course.type=kwargs["type"]

            
        if 'parent_code' in kwargs:
            parent_code= kwargs["parent_code"]
            parent=Account.objects.filter(code=parent_code).first()
            if parent is not None:
                course.parent_id=parent.id

        if 'nature' in kwargs:
            course.nature=kwargs["nature"]
        (result,message,course)=course.save()
        return result,message,course
 

class CourseClassRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=CourseClass.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_courseclass"):
                self.objects=CourseClass.objects
                self.my_accounts=self.objects 
            else:
                me_student=StudentRepo(request=request).me
                if me_student is not None:
                    self.objects=me_student.courseclass_set.all()
                
                else:
                    me_teacher=TeacherRepo(request=request).me
                    if me_teacher is not None:
                        self.objects=me_teacher.courseclass_set.all()
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def course_class(self,*args, **kwargs):
        if "course_class_id" in kwargs and kwargs["course_class_id"] is not None:
            return self.objects.filter(pk=kwargs['course_class_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_course_class(self,*args,**kwargs):
        result,message,course_class=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_course_class"):
            message="دسترسی غیر مجاز"
            return result,message,course_class

        course_class=CourseClass()
        if 'name' in kwargs:
            course_class.name=kwargs["name"]
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                course_class.parent_id=kwargs["parent_id"]
        if 'color' in kwargs:
            course_class.color=kwargs["color"]
        if 'code' in kwargs:
            course_class.code=kwargs["code"]
        if 'priority' in kwargs:
            course_class.priority=kwargs["priority"]
        if 'type' in kwargs:
            course_class.type=kwargs["type"]

            
        if 'parent_code' in kwargs:
            parent_code= kwargs["parent_code"]
            parent=Account.objects.filter(code=parent_code).first()
            if parent is not None:
                course_class.parent_id=parent.id

        if 'nature' in kwargs:
            course_class.nature=kwargs["nature"]
        (result,message,course_class)=course_class.save()
        return result,message,course_class

