from .models import WareHouse,WareHouseSheet
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
        
        if len(WareHouse.objects.filter(name=kwargs["name"]))>0:
            message='نام تکراری برای انبار جدید'
            return FAILED,message,None 
        if not self.request.user.has_perm(APP_NAME+".add_warehouse"):
            message="دسترسی غیر مجاز"
            return result,message,warehouse

        warehouse=WareHouse()
        if 'name' in kwargs:
            warehouse.name=kwargs["name"]  
        if 'person_account_id' in kwargs:
            warehouse.person_account_id=kwargs["person_account_id"]
          
        (result,message,warehouse)=warehouse.save()
        return result,message,warehouse
 



class WareHouseSheetRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=WareHouseSheet.objects.filter(id=0)
        self.me_person=PersonRepo(request=request).me
        if self.me_person is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=WareHouseSheet.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "warehouse_id" in kwargs:
            warehouse_id=kwargs["warehouse_id"]
            objects=objects.filter(warehouse_id=warehouse_id)  
        if "invoice_line_item_id" in kwargs:
            invoice_line_item_id=kwargs["invoice_line_item_id"]
            objects=objects.filter(invoice_line__invoice_line_item_id=invoice_line_item_id) 
        if "product_id" in kwargs:
            product_id=kwargs["product_id"]
            objects=objects.filter(invoice_line__invoice_line_item_id=product_id) 
        if "invoice_line_id" in kwargs:
            invoice_line_id=kwargs["invoice_line_id"]
            objects=objects.filter(invoice_line_id=invoice_line_id) 
        if "invoice_id" in kwargs:
            invoice_id=kwargs["invoice_id"]
            objects=objects.filter(invoice_line__invoice_id=invoice_id) 
        return objects.all()
        
    def warehouse_sheet(self,*args, **kwargs):
        if "warehouse_id" in kwargs and kwargs["warehouse_id"] is not None:
            return self.objects.filter(pk=kwargs['warehouse_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_warehouse_sheet(self,*args,**kwargs):
        result,message,warehouse_sheet=FAILED,"",None
        
        
        if not self.request.user.has_perm(APP_NAME+".add_warehousesheet"):
            message="دسترسی غیر مجاز"
            return result,message,warehouse_sheet

        warehouse_sheet=WareHouseSheet()
        warehouse=WareHouse.objects.filter(pk=kwargs["warehouse_id"]).first()
        if warehouse is None:
            message='انبار درست انتخاب نشده است.'
            return result,message,None    
         
        if 'warehouse_id' in kwargs:
            warehouse_sheet.warehouse_id=kwargs["warehouse_id"]  


        if 'invoice_line_id' in kwargs:
            warehouse_sheet.invoice_line_id=kwargs["invoice_line_id"]
          

        if 'col' in kwargs:
            warehouse_sheet.col=kwargs["col"]  


            
        if 'row' in kwargs:
            warehouse_sheet.row=kwargs["row"]  

            
        if 'shelf' in kwargs:
            warehouse_sheet.shelf=kwargs["shelf"]  



        if 'description' in kwargs:
            warehouse_sheet.description=kwargs["description"]  


        if 'direction' in kwargs:
            warehouse_sheet.direction=kwargs["direction"]  


        warehouse_sheet.person=self.me_person
        warehouse_sheet.save()
        if warehouse_sheet.id is not None:
            result=SUCCEED
            message='برگه انبار با موفقیت ذخیره شد.'
        return result,message,warehouse_sheet
 