from .models import WareHouse 
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


class WareHouseRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=WareHouse.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=WareHouse.objects
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
        
    def warehouse(self,*args, **kwargs):
        if "warehouse_id" in kwargs and kwargs["warehouse_id"] is not None:
            return self.objects.filter(pk=kwargs['warehouse_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_warehouse(self,*args,**kwargs):
        result,message,warehouse=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_warehouse"):
            message="دسترسی غیر مجاز"
            return result,message,warehouse

        warehouse=WareHouse()
        if 'name' in kwargs:
            warehouse.name=kwargs["name"]
        if 'organization_unit_id' in kwargs:
            warehouse.organization_unit_id=kwargs["organization_unit_id"]
        if 'account_id' in kwargs:
            warehouse.account_id=kwargs["account_id"]
          
        (result,message,warehouse)=warehouse.save()
        return result,message,warehouse
 