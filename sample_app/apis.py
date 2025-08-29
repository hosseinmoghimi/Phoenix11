
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import SampleClassRepo
from .serializers import SampleClassSerializer
 
from django.http import JsonResponse
from .forms import *
   
 
class AddSampleClassApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_sample_class_form=AddSampleClassForm(request.POST)
        if add_sample_class_form.is_valid():
            log=333
            cd=add_sample_class_form.cleaned_data
            result,message,sample_class=SampleClassRepo(request=request).add_sample_class(**cd)
            if result==SUCCEED:
                context['sample_class']=SampleClassSerializer(sample_class).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
   