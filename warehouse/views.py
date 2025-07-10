from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from .repo import WareHouseRepo
from .serializers import WareHouseSerializer
from django.views import View
from .forms import *
from .apps import APP_NAME
from core.views import CoreContext
from phoenix.server_apps import phoenix_apps
from utility.calendar import PersianCalendar
from organization.views import OrganizationUnitRepo,OrganizationUnitSerializer
import json
from utility.enums import UnitNameEnum
from utility.log import leolog
from accounting.views import AddInvoiceLineContext,InvoiceContext,ProductContext
LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='warehouse/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"
 
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context

 
 
class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        phoenix_apps = sorted(phoenix_apps, key=lambda d: d['priority'])

        context['phoenix_apps']=phoenix_apps
        return render(request,TEMPLATE_ROOT+"index.html",context)
# Create your views here. 

 
 
class WareHousesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        warehouses=WareHouseRepo(request=request).list(*args, **kwargs)
        context["warehouses"]=warehouses
        warehouses_s=json.dumps(WareHouseSerializer(warehouses,many=True).data)
        context["warehouses_s"]=warehouses_s
        if request.user.has_perm(APP_NAME+'.add_warehouse'):
            context['add_warehouse_form']=AddWareHouseForm()
            organization_units = OrganizationUnitRepo(request=request).list(*args, **kwargs)

            context['organization_units']=organization_units
            organization_units_s=json.dumps(OrganizationUnitSerializer(organization_units,many=True).data)
            context['organization_units_s']=organization_units_s
        return render(request,TEMPLATE_ROOT+"warehouses.html",context)
# Create your views here. 
   
 
class WareHouseView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        warehouse=WareHouseRepo(request=request).warehouse(*args, **kwargs)
        context["warehouse"]=warehouse
        warehouse_s=json.dumps(WareHouseSerializer(warehouse,many=False).data)
        context["warehouse_s"]=warehouse_s

        return render(request,TEMPLATE_ROOT+"warehouse.html",context)
# Create your views here. 


 