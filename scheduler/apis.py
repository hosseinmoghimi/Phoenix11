
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import AppointmentRepo
from .serializers import AppointmentSerializer
 
from django.http import JsonResponse
from .forms import *
   
 
class AddAppointmentApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
        add_appointment_form=AddAppointmentForm(request.POST)
        if add_appointment_form.is_valid():
            log=333
            cd=add_appointment_form.cleaned_data
            result,message,appointment=AppointmentRepo(request=request).add_appointment(**cd)
            if result==SUCCEED:
                context['appointment']=AppointmentSerializer(appointment).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
   