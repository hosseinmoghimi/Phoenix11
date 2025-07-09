
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import WareHouseRepo
from .serializers import WareHouseSerializer
 
from django.http import JsonResponse
from .forms import *
   
 
class AddWareHouseApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
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
   