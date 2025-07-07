from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from django.views import View
from .forms import *
from .serializers import OrganizationSerializer
from .repo import OrganizationRepo
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


def OrganizationContext(request,food_item,*args, **kwargs):
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

  
class OrganizationView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        phoenix_apps = sorted(phoenix_apps, key=lambda d: d['priority'])

        return render(request,TEMPLATE_ROOT+"organization.html",context)
# Create your views here. 

  
  
class OrganizationsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        organizations = OrganizationRepo(request=request).list(*args, **kwargs)

        context['organizations']=organizations
        organizations_s=json.dumps(OrganizationSerializer(organizations,many=True).data)
        context['organizations_s']=organizations_s
        if request.user.has_perm(APP_NAME+".add_organization"):
            context['add_organization_form']=AddOrganizationForm
        return render(request,TEMPLATE_ROOT+"organizations.html",context)
# Create your views here. 

  