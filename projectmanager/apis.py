
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import ProjectRepo,RemoteClientRepo
from .serializers import ProjectSerializer,RemoteClientSerializer
from django.http import JsonResponse
from .forms import *
   
 
class AddRemoteClientApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        message=""
        result=FAILED
        log=2
        AddRemoteClientForm_=AddRemoteClientForm(request.POST)
        is_valid=AddRemoteClientForm_.is_valid()
        if not is_valid:
            message='داده های فرم مجاز نیستند.'
        if is_valid:
            log=3  
            cd=AddRemoteClientForm_.cleaned_data
            result,message,remote_client=RemoteClientRepo(request=request).add_remote_client(**cd)
            if remote_client is not None:
                context['remote_client']=RemoteClientSerializer(remote_client).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 
 
class AddProjectApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
        add_project_form=AddProjectForm(request.POST)
        if add_project_form.is_valid():
            log=333
            cd=add_project_form.cleaned_data
            result,message,project=ProjectRepo(request=request).add_project(**cd)
            if project is not None:
                context['project']=ProjectSerializer(project).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 