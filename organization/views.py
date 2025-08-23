from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from django.views import View
from .forms import *
from .serializers import OrganizationUnitSerializer,EmployeeSerializer
from .repo import OrganizationUnitRepo,EmployeeRepo
from .apps import APP_NAME
from core.views import CoreContext,PageContext,MessageView
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


def OrganizationUnitContext(request,organization_unit,*args, **kwargs):
    context=PageContext(request=request,page=organization_unit)
    context['organization_unit']=organization_unit

    return context
  
 
def organization_unit_employees_link(organization_unit):
    result=''
    for employee in organization_unit.employee_set.all():
        result+=f"""
        <a title="{employee.person.full_name}" href="{employee.get_absolute_url()}">
        <div class='text-center'>
        <img class="rounded-circle" width="64" src="{employee.person.image()}">
        </div>
        <div class='text-center'>
              <small class="text-muted mr-1">{employee.job_title}</small>
        </div>
        </a>
        """
    return result


def AddEmployeeContext(request,*args, **kwargs):
    context={}
    if request.user.has_perm(APP_NAME+".add_employee"):
        context['add_employee_form']=AddEmployeeForm()
        if 'organization_unit' in kwargs:
            organization_unit=kwargs['organization_unit']
            organization_units=[organization_unit]
        else:
            organization_units=OrganizationUnitRepo(request=request).list()
        context['organization_units_for_add_employee_form']=organization_units
    return context
  

class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps

        return render(request,TEMPLATE_ROOT+"index.html",context)

  
class OrganizationUnitView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        organization_unit=OrganizationUnitRepo(request=request).organization_unit(*args, **kwargs)
        context.update(OrganizationUnitContext(request=request,organization_unit=organization_unit))

        employees = organization_unit.employee_set.all()
        context['employees']=employees
        employees_s=json.dumps(EmployeeSerializer(employees,many=True).data)
        context['employees_s']=employees_s



        
        organization_units = OrganizationUnitRepo(request=request).list(parent_id=organization_unit.id)
        context['organization_units']=organization_units
        organization_units_s=json.dumps(OrganizationUnitSerializer(organization_units,many=True).data)
        context['organization_units_s']=organization_units_s
        if request.user.has_perm(APP_NAME+'.add_organizationunit'):
            context['add_organization_unit_form']=AddOrganizationUnitForm()


  
  
        if request.user.has_perm(APP_NAME+".add_employee"):
            context.update(AddEmployeeContext(request=request,organization_unit=organization_unit))

        return render(request,TEMPLATE_ROOT+"organization-unit.html",context)


class OrganizationUnitsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        organization_units = OrganizationUnitRepo(request=request).list(parent_id=None)

        context['organization_units']=organization_units
        organization_units_s=json.dumps(OrganizationUnitSerializer(organization_units,many=True).data)
        context['organization_units_s']=organization_units_s
        if request.user.has_perm(APP_NAME+".add_organization_unit"):
            context['add_organization_unit_form']=AddOrganizationUnitForm
        return render(request,TEMPLATE_ROOT+"organization-units.html",context)


class EmployeeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        employee=EmployeeRepo(request=request).employee(*args, **kwargs)
        if employee is None:
            cc={
                'title':'',
                'body':'',
            }
            mv=MessageView(**cc)
            return mv.get(request=request)
        context['employee']=employee
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        phoenix_apps = sorted(phoenix_apps, key=lambda d: d['priority'])
        return render(request,TEMPLATE_ROOT+"employee.html",context)


class EmployeesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        employees = EmployeeRepo(request=request).list(*args, **kwargs)

        context['employees']=employees
        employees_s=json.dumps(EmployeeSerializer(employees,many=True).data)
        context['employees_s']=employees_s
        if request.user.has_perm(APP_NAME+".add_employee"):
            context.update(AddEmployeeContext(request=request))
             
        return render(request,TEMPLATE_ROOT+"employees.html",context)

  
class TreeChartView(View):
    
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        organization_unit=OrganizationUnitRepo(request=request).organization_unit(*args, **kwargs)
        if organization_unit is None:
            title='واحد سازمانی وجود ندارد'
            body='واحد سازمانی وجود ندارد'
            mv=MessageView(title=title,body=body)
            return mv.get(request=request)
        
        context['organization_unit']=organization_unit  


        organization_units=organization_unit.all_sub_organization_units()
        context['organization_units']=organization_units
        organization_units_s=json.dumps(OrganizationUnitSerializer(organization_units,many=True).data)
        context['organization_units_s']=organization_units_s

        
        context['WIDE_LAYOUT']=True 
         
        
        pages=[{
                'title': f"""{organization_unit.title}""",
                'parent_id': organization_unit.parent_id,
                'parent': 0,
                'get_absolute_url': organization_unit.get_absolute_url(),
                'id': organization_unit.id,
                'pre_title': "",
                'color': organization_unit.color,
                'sub_title':organization_unit_employees_link(organization_unit),
                }]
          
        for organization_unit in organization_units:
            pages.append({
                'title': f"""{organization_unit.title}""",
                'parent_id': organization_unit.parent_id,
                'parent': 0,
                'get_absolute_url': organization_unit.get_absolute_url(),
                'id': organization_unit.id,
                'pre_title': "",
                'color': organization_unit.color,
                'sub_title':organization_unit_employees_link(organization_unit),
                })

        context['pages_s'] = json.dumps(pages)
        return render(request,TEMPLATE_ROOT+"tree-chart.html",context) 
