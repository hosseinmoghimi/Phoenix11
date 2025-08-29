
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import TrafficRepo
from .serializers import TrafficSerializer
 
from django.http import JsonResponse
from .forms import *
   
 
class AddTrafficApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_traffic_form=AddTrafficForm(request.POST)
        if add_traffic_form.is_valid():
            log=333
            cd=add_traffic_form.cleaned_data
            result,message,traffic=TrafficRepo(request=request).add_traffic(**cd)
            if result==SUCCEED:
                context['traffic']=TrafficSerializer(traffic).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
   