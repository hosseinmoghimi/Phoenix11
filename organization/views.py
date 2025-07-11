from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from django.views import View
from .forms import *
from .serializers import OrganizationUnitSerializer,EmployeeSerializer
from .repo import OrganizationUnitRepo,EmployeeRepo
from .apps import APP_NAME
from core.views import CoreContext,PageContext
from utility.calendar import PersianCalendar
import json
from utility.enums import UnitNameEnum
from utility.log import leolog
from accounting.views import ProductContext,PageContext
LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='organization/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"
 
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context


def OrganizationUnitContext(request,food_item,*args, **kwargs):
    context=PageContext(request=request,page=food_item)
    return context
  
 
 
class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps

        return render(request,TEMPLATE_ROOT+"index.html",context)
# Create your views here. 

  
class OrganizationUnitView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        organization_unit=OrganizationUnitRepo(request=request).organization_unit(*args, **kwargs)
        context['organization_unit']=organization_unit

        employees = organization_unit.employee_set.all()

        context['employees']=employees
        employees_s=json.dumps(EmployeeSerializer(employees,many=True).data)
        context['employees_s']=employees_s

        return render(request,TEMPLATE_ROOT+"organization-unit.html",context)
# Create your views here. 

  
  
class OrganizationUnitsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        organization_units = OrganizationUnitRepo(request=request).list(*args, **kwargs)

        context['organization_units']=organization_units
        organization_units_s=json.dumps(OrganizationUnitSerializer(organization_units,many=True).data)
        context['organization_units_s']=organization_units_s
        if request.user.has_perm(APP_NAME+".add_organization_unit"):
            context['add_organization_unit_form']=AddOrganizationUnitForm
        return render(request,TEMPLATE_ROOT+"organization-units.html",context)
# Create your views here. 

  
class EmployeeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        phoenix_apps = sorted(phoenix_apps, key=lambda d: d['priority'])

        return render(request,TEMPLATE_ROOT+"employee.html",context)
# Create your views here. 

  
  
class EmployeesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        employees = EmployeeRepo(request=request).list(*args, **kwargs)

        context['employees']=employees
        employees_s=json.dumps(EmployeeSerializer(employees,many=True).data)
        context['employees_s']=employees_s
        if request.user.has_perm(APP_NAME+".add_employee"):
            context['add_employee_form']=AddEmployeeForm
            organization_units=OrganizationUnitRepo(request=request).list()
            context['organization_units_for_add_employee_form']=organization_units
        return render(request,TEMPLATE_ROOT+"employees.html",context)
# Create your views here. 

  