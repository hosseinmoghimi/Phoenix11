
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import OrganizationUnitRepo,EmployeeRepo
from .serializers import OrganizationUnitSerializer,EmployeeSerializer
from django.http import JsonResponse
from .forms import *
   
 
class AddEmployeeApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
        add_employee_form=AddEmployeeForm(request.POST)
        if add_employee_form.is_valid():
            log=333
            cd=add_employee_form.cleaned_data
            result,message,employee=EmployeeRepo(request=request).add_employee(**cd)
            if employee is not None:
                context['employee']=EmployeeSerializer(employee).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 
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
            if result==SUCCEED:
                context['organization_unit']=OrganizationUnitSerializer(organization_unit).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 



 
 
class SelectOrganizationUnitApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            select_organization_unit_form=SelectOrganizationUnitForm(request.POST)
            if select_organization_unit_form.is_valid():
                log=333
                cd=select_organization_unit_form.cleaned_data
                organization_unit=OrganizationUnitRepo(request=request).organization_unit(**cd)
                if organization_unit is not None:
                    result=SUCCEED
                    message="موفقیت آمیز"
                    context['organization_unit']=OrganizationUnitSerializer(organization_unit).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


 

 
class SelectEmployeeApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            select_employee_form=SelectEmployeeForm(request.POST)
            if select_employee_form.is_valid():
                log=333
                cd=select_employee_form.cleaned_data
                employee=EmployeeRepo(request=request).employee(**cd)
                if employee is not None:
                    result=SUCCEED
                    message="موفقیت آمیز"
                    context['employee']=EmployeeSerializer(employee).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


 