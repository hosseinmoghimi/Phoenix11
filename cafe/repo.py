from .models import Table
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


class TableRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Table.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=Table.objects
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
        
    def table(self,*args, **kwargs):
        if "table_id" in kwargs and kwargs["table_id"] is not None:
            return self.objects.filter(pk=kwargs['table_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_table(self,*args,**kwargs):
        result,message,table=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_table"):
            message="دسترسی غیر مجاز"
            return result,message,table

        table=Table()
        if 'title' in kwargs:
            table.title=kwargs["title"]
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                table.parent_id=kwargs["parent_id"]
        if 'color' in kwargs:
            table.color=kwargs["color"]
        if 'code' in kwargs:
            table.code=kwargs["code"]
        if 'priority' in kwargs:
            table.priority=kwargs["priority"]
        if 'table_no' in kwargs:
            table.table_no=kwargs["table_no"]
 

        if 'nature' in kwargs:
            table.nature=kwargs["nature"]
        table.save()
        if table.id is not None and table.id>0:
            message='با موفقیت ذخیره شد.'
            result=SUCCEED
            return result,message,table
        else:
            return result,message,None

 