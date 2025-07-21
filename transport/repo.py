from .models import Vehicle,MaintenanceInvoice

from .apps import APP_NAME
from .enums import *
from log.repo import LogRepo 
from django.db.models import Q
from django.shortcuts import reverse
from authentication.repo import ProfileRepo
from utility.constants import FAILED,SUCCEED
from utility.log import leolog


class VehicleRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Vehicle.objects.filter(id=0)
        profile=ProfileRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_vehicle"):
                self.objects=Vehicle.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def vehicle(self,*args, **kwargs):
        if "vehicle_id" in kwargs and kwargs["vehicle_id"] is not None:
            return self.objects.filter(pk=kwargs['vehicle_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_vehicle(self,*args,**kwargs):
        result,message,vehicle=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_vehicle"):
            message="دسترسی غیر مجاز"
            return result,message,vehicle

        vehicle=Vehicle()
        if 'title' in kwargs:
            vehicle.title=kwargs["title"]
          
        (result,message,vehicle)=vehicle.save()
        return result,message,vehicle


  
class MaintenanceInvoiceRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=MaintenanceInvoice.objects.filter(id=0)
        profile=ProfileRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_maintenance_invoice"):
                self.objects=MaintenanceInvoice.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def maintenance_invoice(self,*args, **kwargs):
        if "maintenance_invoice_id" in kwargs and kwargs["maintenance_invoice_id"] is not None:
            return self.objects.filter(pk=kwargs['maintenance_invoice_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_maintenance_invoice(self,*args,**kwargs):
        result,message,maintenance_invoice=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_maintenance_invoice"):
            message="دسترسی غیر مجاز"
            return result,message,maintenance_invoice

        maintenance_invoice=MaintenanceInvoice()
        if 'title' in kwargs:
            maintenance_invoice.title=kwargs["title"]
        if 'kilometer' in kwargs:
            maintenance_invoice.kilometer=kwargs["kilometer"]
        if 'service_man_id' in kwargs:
            maintenance_invoice.service_man_id=kwargs["service_man_id"]
        if 'vehicle_id' in kwargs:
            maintenance_invoice.vehicle_id=kwargs["vehicle_id"]
            
        if 'color' in kwargs:
            maintenance_invoice.color=kwargs["color"]
        if 'code' in kwargs:
            maintenance_invoice.code=kwargs["code"]
        if 'priority' in kwargs:
            maintenance_invoice.priority=kwargs["priority"]
        if 'bedehkar_id' in kwargs:
            maintenance_invoice.bedehkar_id=kwargs["bedehkar_id"]
        if 'bestankar_id' in kwargs:
            maintenance_invoice.bestankar_id=kwargs["bestankar_id"]
        if 'event_datetime' in kwargs:
            
            year=kwargs['event_datetime'][:2]
            if year=="13" or year=="14":
                from utility.calendar import PersianCalendar
                kwargs['event_datetime']=PersianCalendar().to_gregorian(kwargs["event_datetime"])
            maintenance_invoice.event_datetime=kwargs["event_datetime"]

        if 'type' in kwargs:
            maintenance_invoice.type=kwargs["type"]

           
           
        (result,message,maintenance_invoice)=maintenance_invoice.save()
        return result,message,maintenance_invoice
    