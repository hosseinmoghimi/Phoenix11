
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import TaxRepo
from .serializers import TaxSerializer
 
from django.http import JsonResponse
from .forms import *
   
 
class AddTaxApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_school_form=AddTaxForm(request.POST)
        if add_school_form.is_valid():
            log=333
            cd=add_school_form.cleaned_data
            result,message,school=TaxRepo(request=request).add_school(**cd)
            if school is not None:
                context['school']=TaxSerializer(school).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
   