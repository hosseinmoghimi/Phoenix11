
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import OrganizationRepo
from .serializers import OrganizationSerializer
from django.http import JsonResponse
from .forms import *
   
 
class AddOrganizationApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
        add_organization_form=AddOrganizationForm(request.POST)
        if add_organization_form.is_valid():
            log=333
            cd=add_organization_form.cleaned_data
            result,message,organization=OrganizationRepo(request=request).add_organization(**cd)
            if organization is not None:
                context['organization']=OrganizationSerializer(organization).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 