
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import PollRepo
from .serializers import PollSerializer
 
from django.http import JsonResponse
from .forms import *
   
 
class AddPollApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
        add_poll_form=AddPollForm(request.POST)
        if add_poll_form.is_valid():
            log=333
            cd=add_poll_form.cleaned_data
            result,message,poll=PollRepo(request=request).add_poll(**cd)
            if result==SUCCEED:
                context['poll']=PollSerializer(poll).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
   