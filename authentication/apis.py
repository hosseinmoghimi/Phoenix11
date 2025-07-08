
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import PersonRepo
from .serializer import PersonSerializer
from django.http import JsonResponse
from .forms import *
   

class AddPersonApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
        add_person_form=AddPersonForm(request.POST)
        if add_person_form.is_valid():
            log=333
            cd=add_person_form.cleaned_data
            result,message,person=PersonRepo(request=request).add_person(**cd)
            if person is not None:
                context['person']=PersonSerializer(person).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 