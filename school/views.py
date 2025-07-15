from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from .repo import CourseRepo,SchoolRepo,CourseClassRepo
from .serializers import CourseClassSerializer,SchoolSerializer,CourseSerializer
from django.views import View
from .forms import *
from .apps import APP_NAME
from core.views import CoreContext
from phoenix.server_apps import phoenix_apps
from utility.calendar import PersianCalendar
import json
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

 
 
class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        phoenix_apps = sorted(phoenix_apps, key=lambda d: d['priority'])

        context['phoenix_apps']=phoenix_apps
        return render(request,TEMPLATE_ROOT+"index.html",context)
# Create your views here. 

 
 
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

        return render(request,TEMPLATE_ROOT+"course.html",context)
# Create your views here. 



class CourseClassesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        course_classs=CourseClassRepo(request=request).list(*args, **kwargs)
        context["course_classs"]=course_classs
        course_classs_s=json.dumps(CourseClassSerializer(course_classs,many=True).data)
        context["course_classs_s"]=course_classs_s

        return render(request,TEMPLATE_ROOT+"course-classes.html",context)
# Create your views here. 
   
 
class CourseClassView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        course_class=CourseClassRepo(request=request).course_class(*args, **kwargs)
        context["course_class"]=course_class
        course_class_s=json.dumps(CourseClassSerializer(course_class,many=False).data)
        context["course_class_s"]=course_class_s

        return render(request,TEMPLATE_ROOT+"course-class.html",context)
# Create your views here. 

 