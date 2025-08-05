from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from .serializers import VehicleSerializer,MaintenanceInvoiceSerializer,ServiceManSerializer
from .repo import VehicleRepo,MaintenanceInvoiceRepo,ServiceManRepo
from .forms import *
from .apps import APP_NAME
from phoenix.server_apps import phoenix_apps
from utility.calendar import PersianCalendar
import json
from django.views import View
from core.views import CoreContext,leolog
from accounting.views import AssetContext,AddInvoiceContext,InvoiceSerializer
from .enums import MaintenanceTypesEnum
LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='transport/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"
 

def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
    context[WIDE_LAYOUT]=False 
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context

def AddMaintenanceInvoiceContext(request,*args, **kwargs):
    context=AddInvoiceContext(request=request)
    context['add_maintenance_invoice_form']=AddMaintenanceInvoiceForm()
    context['maintenance_types']=(i[0] for i in MaintenanceTypesEnum.choices)
    return context


def VehicleContext(request,vehicle,*args, **kwargs):
    context=AssetContext(request=request,asset=vehicle)
    if request.user.has_perm('accounting.add_invoice'):
        context.update(AddMaintenanceInvoiceContext(request=request))
    maintenance_invoices=MaintenanceInvoiceRepo(request=request).list(vehicle_id=vehicle.id)
    maintenance_invoices_s=json.dumps(MaintenanceInvoiceSerializer(maintenance_invoices,many=True).data)
    context['maintenance_invoices']=maintenance_invoices
    context['maintenance_invoices_s']=maintenance_invoices_s





    service_mans=ServiceManRepo(request=request).list(vehicle_id=vehicle.id)
    service_mans_s=json.dumps(ServiceManSerializer(service_mans,many=True).data)
    context['service_mans']=service_mans
    context['service_mans_s']=service_mans_s

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

 

class VehiclesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        vehicles =VehicleRepo(request=request).list(*args, **kwargs)
        context['vehicles']=vehicles
        vehicles_s=json.dumps(VehicleSerializer(vehicles,many=True).data)
        context['vehicles_s']=vehicles_s
 
        context[WIDE_LAYOUT]=False
        if request.user.has_perm(APP_NAME+'.add_vehicle'):
            context['add_vehicle_form']=AddVehicleForm()
        return render(request,TEMPLATE_ROOT+"vehicles.html",context) 
    
    
    
class VehicleView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        vehicle =VehicleRepo(request=request).vehicle(*args, **kwargs)
        context[WIDE_LAYOUT]=False
        context['vehicle']=vehicle 
        context.update(VehicleContext(request=request,vehicle=vehicle))
        return render(request,TEMPLATE_ROOT+"vehicle.html",context) 
    
 

class MaintenanceInvoicesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        maintenance_invoices =MaintenanceInvoiceRepo(request=request).list(*args, **kwargs)
        context['maintenance_invoices']=maintenance_invoices
        maintenance_invoices_s=json.dumps(MaintenanceInvoiceSerializer(maintenance_invoices,many=True).data)
        context['maintenance_invoices_s']=maintenance_invoices_s
 
        context[WIDE_LAYOUT]=False
        if request.user.has_perm(APP_NAME+'.add_maintenanceinvoice'):
            context['add_maintenance_invoice_form']=AddMaintenanceInvoiceForm()
        return render(request,TEMPLATE_ROOT+"maintenance-invoices.html",context) 
    
    
    
class MaintenanceInvoiceView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        maintenance_invoice =MaintenanceInvoiceRepo(request=request).maintenance_invoice(*args, **kwargs)
        context[WIDE_LAYOUT]=False
        context['maintenance_invoice']=maintenance_invoice
        from accounting.views import InvoiceContext
        context.update(InvoiceContext(request=request,invoice=maintenance_invoice))
        return render(request,TEMPLATE_ROOT+"maintenance-invoice.html",context) 
    
 
 

class ServiceMansView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        service_mans =ServiceManRepo(request=request).list(*args, **kwargs)
        context['service_mans']=service_mans
        service_mans_s=json.dumps(ServiceManSerializer(service_mans,many=True).data)
        context['service_mans_s']=service_mans_s
 
        context[WIDE_LAYOUT]=False
        if request.user.has_perm(APP_NAME+'.add_serviceman'):
            context['add_service_man_form']=AddServiceManForm()
        return render(request,TEMPLATE_ROOT+"service-mans.html",context) 
    
    
 
    
class ServiceManView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        service_man =ServiceManRepo(request=request).service_man(*args, **kwargs)
        context[WIDE_LAYOUT]=False
        context['service_man']=service_man


        maintenance_invoices =MaintenanceInvoiceRepo(request=request).list(service_man_id=service_man.id)
        context['maintenance_invoices']=maintenance_invoices
        maintenance_invoices_s=json.dumps(MaintenanceInvoiceSerializer(maintenance_invoices,many=True).data)
        context['maintenance_invoices_s']=maintenance_invoices_s
 

        return render(request,TEMPLATE_ROOT+"service-man.html",context) 
    
