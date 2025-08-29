
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import PersonRepo,PersonRepo
from .serializers import PersonSerializer
from django.http import JsonResponse
from .forms import *
   

class AddPersonApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_person_form=AddPersonForm(request.POST)
        if add_person_form.is_valid():
            log=333
            cd=add_person_form.cleaned_data
            result,message,person=PersonRepo(request=request).add_person(**cd)
            if person is not None:
                context['person']=PersonSerializer(person).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 

class SelectPersonApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        select_person_form=SelectPersonForm(request.POST)
        if select_person_form.is_valid():
            log=333
            cd=select_person_form.cleaned_data
            person=PersonRepo(request=request).person(**cd)
            if person is not None:
                context['person']=PersonSerializer(person).data
                result=SUCCEED
                message='موفق'
            else:
                message='شخص پیدا نشد.'
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 

class SelectUserApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        select_person_form=SelectUserForm(request.POST)
        if select_person_form.is_valid():
            log=333
            cd=select_person_form.cleaned_data
            user=PersonRepo(request=request).user(**cd)
            if user is not None:
                context['username']=user.username
                result=SUCCEED
                message='موفق'
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 
class SelectProfileApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        select_profile_form=SelectProfileForm(request.POST)
        if select_profile_form.is_valid():
            log=333
            cd=select_profile_form.cleaned_data
            profile=PersonRepo(request=request).profile(**cd)
            if profile is not None:
                context['profile']=ProfileSerializer(profile).data
                message='موفق'
                result=SUCCEED
        context['result']=result
        context['message']=message
        context['log']=log
        return JsonResponse(context)
 