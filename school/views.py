from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from .repo import CourseRepo,SchoolRepo,CourseClassRepo,TeacherRepo,StudentRepo,MajorRepo
from .serializers import CourseClassSerializer,SchoolSerializer,CourseSerializer,TeacherSerializer,StudentSerializer,MajorSerializer
from django.views import View
from .forms import *
from .apps import APP_NAME
from core.views import CoreContext
from phoenix.server_apps import phoenix_apps
from utility.calendar import PersianCalendar
import json
from library.serializers import BookSerializer

from utility.enums import UnitNameEnum
from utility.log import leolog
from accounting.views import AddInvoiceLineContext,InvoiceContext,ProductContext
LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='school/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"
 
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context

def AddCourseClassContext(request,*args, **kwargs):
    context={}
    context['add_course_class_form']=AddCourseClassForm()
    return context
 
class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        phoenix_apps = sorted(phoenix_apps, key=lambda d: d['priority'])

        context['phoenix_apps']=phoenix_apps
        return render(request,TEMPLATE_ROOT+"index.html",context)

def AddTeacherContext(request):
    context={}
    context['add_teacher_form']=AddTeacherForm()
    return context

def AddMajorContext(request):
    context={}
    context['add_major_form']=AddMajorForm()
    return context

class TeachersView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        teachers=TeacherRepo(request=request).list(*args, **kwargs)
        context["teachers"]=teachers
        teachers_s=json.dumps(TeacherSerializer(teachers,many=True).data)
        context["teachers_s"]=teachers_s
        if request.user.has_perm(APP_NAME+'.add_teacher'):
            context.update(AddTeacherContext(request=request))
        return render(request,TEMPLATE_ROOT+"teachers.html",context)
# Create your views here. 
   
class StudentsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        students=StudentRepo(request=request).list(*args, **kwargs)
        context["students"]=students
        students_s=json.dumps(StudentSerializer(students,many=True).data)
        context["students_s"]=students_s
        if request.user.has_perm(APP_NAME+'.add_student'):
            context['add_student_form']=AddStudentForm()
        return render(request,TEMPLATE_ROOT+"students.html",context)
# Create your views here. 
   
 
 
class StudentView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        student=StudentRepo(request=request).student(*args, **kwargs)
        context["student"]=student
        student_s=json.dumps(StudentSerializer(student,many=False).data)
        context["student_s"]=student_s

        return render(request,TEMPLATE_ROOT+"student.html",context)
 
 
class TeacherView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        teacher=TeacherRepo(request=request).teacher(*args, **kwargs)
        context["teacher"]=teacher
        teacher_s=json.dumps(TeacherSerializer(teacher,many=False).data)
        context["teacher_s"]=teacher_s

        return render(request,TEMPLATE_ROOT+"teacher.html",context)
class SchoolsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        schools=SchoolRepo(request=request).list(*args, **kwargs)
        context["schools"]=schools
        schools_s=json.dumps(SchoolSerializer(schools,many=True).data)
        context["schools_s"]=schools_s
        if request.user.has_perm(APP_NAME+'.add_school'):
            context['add_school_form']=AddSchoolForm()
        return render(request,TEMPLATE_ROOT+"schools.html",context)
# Create your views here. 
   
 
class SchoolView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        school=SchoolRepo(request=request).school(*args, **kwargs)
        context["school"]=school
        school_s=json.dumps(SchoolSerializer(school,many=False).data)
        context["school_s"]=school_s

        return render(request,TEMPLATE_ROOT+"school.html",context)
# Create your views here. 



 
class CoursesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        courses=CourseRepo(request=request).list(*args, **kwargs)
        context["courses"]=courses
        courses_s=json.dumps(CourseSerializer(courses,many=True).data)
        context["courses_s"]=courses_s
        if request.user.has_perm(APP_NAME+'.add_course'):
            context['add_course_form']=AddCourseForm()
        return render(request,TEMPLATE_ROOT+"courses.html",context)
# Create your views here. 
   
 
class CourseView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        course=CourseRepo(request=request).course(*args, **kwargs)
        context["course"]=course
        course_s=json.dumps(CourseSerializer(course,many=False).data)
        context["course_s"]=course_s


        books=course.books.all()
        context["books"]=books
        books_s=json.dumps(BookSerializer(books,many=True).data)
        context["books_s"]=books_s


        return render(request,TEMPLATE_ROOT+"course.html",context)
# Create your views here. 




class MajorView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        major=MajorRepo(request=request).major(*args, **kwargs)
        context["major"]=major
        major_s=json.dumps(MajorSerializer(major,many=False).data)
        context["major_s"]=major_s

        return render(request,TEMPLATE_ROOT+"major.html",context)
# Create your views here. 




class CourseClassesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        course_classes=CourseClassRepo(request=request).list(*args, **kwargs)
        context["course_classes"]=course_classes
        course_classes_s=json.dumps(CourseClassSerializer(course_classes,many=True).data)
        context["course_classes_s"]=course_classes_s
        if request.user.has_perm(APP_NAME+'.add_courseclass'):
            context.update(AddCourseClassContext(request=request))
        return render(request,TEMPLATE_ROOT+"course-classes.html",context)
# Create your views here. 
   


   
class MajorsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        majors=MajorRepo(request=request).list(*args, **kwargs)
        context["majors"]=majors
        majors_s=json.dumps(MajorSerializer(majors,many=True).data)
        context["majors_s"]=majors_s
        if request.user.has_perm(APP_NAME+'.add_major'):
            context.update(AddMajorContext(request=request))
        return render(request,TEMPLATE_ROOT+"majors.html",context)
# Create your views here. 
   
 
class CourseClassView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        course_class=CourseClassRepo(request=request).course_class(*args, **kwargs)
        context["course_class"]=course_class
        course_class_s=json.dumps(CourseClassSerializer(course_class,many=False).data)
        context["course_class_s"]=course_class_s


        books=course_class.course.books.all()
        context["books"]=books
        books_s=json.dumps(BookSerializer(books,many=True).data)
        context["books_s"]=books_s
        
        teachers=course_class.teachers.all()
        context["teachers"]=teachers
        teachers_s=json.dumps(TeacherSerializer(teachers,many=True).data)
        context["teachers_s"]=teachers_s
 



        
        students=course_class.students.all()
        context["students"]=students
        students_s=json.dumps(StudentSerializer(students,many=True).data)
        context["students_s"]=students_s
 

        return render(request,TEMPLATE_ROOT+"course-class.html",context)
# Create your views here. 

 