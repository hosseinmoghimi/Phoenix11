from .models import Traffic
from .apps import APP_NAME
from .enums import *
from log.repo import LogRepo 
from django.db.models import Q
from django.shortcuts import reverse
from authentication.repo import PersonRepo
from accounting.repo import InvoiceLineItemUnitRepo
from utility.num import filter_number
from utility.calendar import PersianCalendar
from utility.constants import FAILED,SUCCEED
from utility.log import leolog
from .enums import *


class TrafficRepo():

    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Traffic.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=Traffic.objects
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
        
    def traffic(self,*args, **kwargs):
        if "traffic_id" in kwargs and kwargs["traffic_id"] is not None:
            return self.objects.filter(pk=kwargs['traffic_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_traffic(self,*args,**kwargs):
        result,message,traffic=FAILED,"",None
        if len(Traffic.objects.filter(name=kwargs["name"]))>0:
            message='نام تکراری برای آموزشگاه جدید'
            return FAILED,message,None
        if len(Traffic.objects.filter(person_account_id=kwargs["person_account_id"]))>0:
            message='حساب تکراری برای آموزشگاه جدید'
            return FAILED,message,None
        if not self.request.user.has_perm(APP_NAME+".add_traffic"):
            message="دسترسی غیر مجاز"
            return result,message,traffic

        traffic=Traffic() 
        if 'person_account_id' in kwargs:
            traffic.person_account_id=kwargs["person_account_id"]
        if 'name' in kwargs:
            traffic.name=kwargs["name"]
          
        (result,message,traffic)=traffic.save()
        return result,message,traffic