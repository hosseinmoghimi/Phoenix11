
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import DrugRepo
from .serializers import DrugSerializer
from django.http import JsonResponse
from .forms import *
   


class AddDrugApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
        add_drug_form=AddDrugForm(request.POST)
        if add_drug_form.is_valid():
            log=333
            cd=add_drug_form.cleaned_data
            result,message,drug=DrugRepo(request=request).add_drug(**cd)
            if drug is not None:
                context['drug']=DrugSerializer(drug).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 