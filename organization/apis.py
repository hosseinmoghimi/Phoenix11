
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import OrganizationUnitRepo
from .serializers import OrganizationUnitSerializer
from django.http import JsonResponse
from .forms import *
   
 
class AddOrganizationUnitApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
        add_organization_unit_form=AddOrganizationUnitForm(request.POST)
        if add_organization_unit_form.is_valid():
            log=333
            cd=add_organization_unit_form.cleaned_data
            result,message,organization_unit=OrganizationUnitRepo(request=request).add_organization_unit(**cd)
            if organization_unit is not None:
                context['organization_unit']=OrganizationUnitSerializer(organization_unit).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 