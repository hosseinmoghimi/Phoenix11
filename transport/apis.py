
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import VehicleRepo,MaintenanceInvoiceRepo
from .serializers import VehicleSerializer,MaintenanceInvoiceSerializer
from django.http import JsonResponse
from .forms import *


class AddVehicleApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
        add_vehicle_form=AddVehicleForm(request.POST)
        if add_vehicle_form.is_valid():
            log=333
            cd=add_vehicle_form.cleaned_data
            result,message,vehicle=VehicleRepo(request=request).add_vehicle(**cd)
            if vehicle is not None:
                context['vehicle']=VehicleSerializer(vehicle).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
  
 


 

class AddMaintenanceInvoiceApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
        add_maintenance_form=AddMaintenanceInvoiceForm(request.POST)
        if add_maintenance_form.is_valid():
            log=333
            cd=add_maintenance_form.cleaned_data
            result,message,maintenance=MaintenanceInvoiceRepo(request=request).add_maintenance_invoice(**cd)
            if maintenance is not None:
                context['maintenance']=MaintenanceInvoiceSerializer(maintenance).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
  
 