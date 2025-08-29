
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import WareHouseRepo,WareHouseSheetRepo
from .serializers import WareHouseSerializer,WareHouseSheetSerializer
 
from django.http import JsonResponse
from .forms import *
   
class SelectWareHouseApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        select_warehouse_form=SelectWareHouseForm(request.POST)
        if select_warehouse_form.is_valid():
            log=333
            cd=select_warehouse_form.cleaned_data
            warehouse_id=cd['warehouse_id']
            warehouse=WareHouseRepo(request=request).warehouse(warehouse_id=warehouse_id)
            message='انبار پیدا نشد.'
            if warehouse is not None:
                context['warehouse']=WareHouseSerializer(warehouse).data
                result=SUCCEED
                message='انبار پیدا شد.'
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
   
 
class AddWareHouseApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_warehouse_form=AddWareHouseForm(request.POST)
        if add_warehouse_form.is_valid():
            log=333
            cd=add_warehouse_form.cleaned_data
            result,message,warehouse=WareHouseRepo(request=request).add_warehouse(**cd)
            if warehouse is not None:
                context['warehouse']=WareHouseSerializer(warehouse).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
    


    
 
class AddWareHouseSheetApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_warehouse_sheet_form=AddWareHouseSheetForm(request.POST)
        if add_warehouse_sheet_form.is_valid():
            log=333
            cd=add_warehouse_sheet_form.cleaned_data
            result,message,warehouse_sheet=WareHouseSheetRepo(request=request).add_warehouse_sheet(**cd)
            if warehouse_sheet is not None:
                context['warehouse_sheet']=WareHouseSheetSerializer(warehouse_sheet).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
   