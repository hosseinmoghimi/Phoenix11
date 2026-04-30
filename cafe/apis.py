
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import TableRepo
from .serializers import TableSerializer
from django.http import JsonResponse
from .forms import *
    
class AddTableApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_table_form=AddTableForm(request.POST)
        if add_table_form.is_valid():
            log=333
            cd=add_table_form.cleaned_data
            result,message,table=TableRepo(request=request).add_table(**cd)
            if table is not None:
                context['table']=TableSerializer(table).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 