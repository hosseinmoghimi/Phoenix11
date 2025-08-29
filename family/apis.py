
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import FamilyRepo
from .serializers import FamilySerializer
 
from django.http import JsonResponse
from .forms import *
   
 
class AddFamilyApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_family_form=AddFamilyForm(request.POST)
        if add_family_form.is_valid():
            log=333
            cd=add_family_form.cleaned_data
            result,message,family=FamilyRepo(request=request).add_family(**cd)
            if result==SUCCEED:
                context['family']=FamilySerializer(family).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
   