
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import SchoolRepo,CourseRepo,CourseClassRepo
from .serializers import SchoolSerializer,CourseSerializer,CourseClassSerializer
 
from django.http import JsonResponse
from .forms import *
   
 
class AddSchoolApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
        add_school_form=AddSchoolForm(request.POST)
        if add_school_form.is_valid():
            log=333
            cd=add_school_form.cleaned_data
            result,message,school=SchoolRepo(request=request).add_school(**cd)
            if school is not None:
                context['school']=SchoolSerializer(school).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
  
 
class AddCourseApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
        add_course_form=AddCourseForm(request.POST)
        if add_course_form.is_valid():
            log=333
            cd=add_course_form.cleaned_data
            result,message,course=CourseRepo(request=request).add_course(**cd)
            if course is not None:
                context['course']=CourseSerializer(course).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
  
class AddCourseClassApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
        add_course_class_form=AddCourseClassForm(request.POST)
        if add_course_class_form.is_valid():
            log=333
            cd=add_course_class_form.cleaned_data
            result,message,course_class=CourseClassRepo(request=request).add_course_class(**cd)
            if course_class is not None:
                context['course_class']=CourseClassSerializer(course_class).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
  