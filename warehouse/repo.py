from organization.repo import EmployeeRepo,OrganizationUnitRepo
from .models import WareHouse,WareHouseSheet,WareHouseSheetSignature,WareHouseSheetLabel
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
from accounting.repo import InvoiceLine,FinancialEventStatusEnum,InvoiceRepo


class WareHouseRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=WareHouse.objects.filter(id=0)
        person=PersonRepo(request=request).me
        me_employee=EmployeeRepo(request=request).me
        if person is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=WareHouse.objects
            elif me_employee is not None:
                self.objects=WareHouse.objects.filter(person_account_id=me_employee.organization_unit.person_account.id)


    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(person_account__person__full_name__contains=search_for)  )
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


class WareHouseSheetLabelRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=WareHouseSheetLabel.objects.filter(id=0)
        self.me_person=PersonRepo(request=request).me
        if self.me_person is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=WareHouseSheetLabel.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "warehouse_id" in kwargs:
            warehouse_id=kwargs["warehouse_id"]
            objects=objects.filter(warehouse_id=warehouse_id) 
        if "warehouse_sheet_id" in kwargs:
            warehouse_sheet_id=kwargs["warehouse_sheet_id"]
            objects=objects.filter(warehouse_sheet_id=warehouse_sheet_id)  
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
        
    def warehouse_sheet_label(self,*args, **kwargs):
        if "warehouse_id" in kwargs and kwargs["warehouse_id"] is not None:
            return self.objects.filter(pk=kwargs['warehouse_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_warehouse_sheet_label(self,*args,**kwargs):
        result,message,warehouse_sheet_label=FAILED,"",None
        
        
        if not self.request.user.has_perm(APP_NAME+".add_warehousesheetlabel"):
            message="دسترسی غیر مجاز"
            return result,message,warehouse_sheet_label

        warehouse_sheet_label=WareHouseSheetLabel()
        warehouse_sheet=WareHouseSheet.objects.filter(pk=kwargs["warehouse_sheet_id"]).first()
        if warehouse_sheet is None:
            message='برگه انبار درست انتخاب نشده است.'
            return result,message,None    
        me_employee=EmployeeRepo(request=self.request).me
        if me_employee is None:
            return FAILED,'شما حق امضا ندارید.',None
        warehouse_sheet_label.employee_id=me_employee.id

            
        if 'warehouse_sheet_id' in kwargs:
            warehouse_sheet_label.warehouse_sheet_id=kwargs["warehouse_sheet_id"]  

        if 'description' in kwargs:
            warehouse_sheet_label.description=kwargs["description"]  


        if 'serial_no' in kwargs:
            warehouse_sheet_label.serial_no=kwargs["serial_no"]  

 
        warehouse_sheet_label.save()
        if warehouse_sheet_label.id is not None:
            result=SUCCEED
            message='امضای برگه انبار با موفقیت ذخیره شد.'
        return result,message,warehouse_sheet_label
 

class WareHouseSheetRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.me_person=PersonRepo(request=request).me
        self.objects=WareHouseSheet.objects.filter(person_id=self.me_person.id)
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
        
    def add_material_request(self,*args, **kwargs):
        result,message,warehouse_sheet,invoice_line=FAILED,"",None,None
        

        me_employee=EmployeeRepo(request=self.request).me
        sw=False
        message="دسترسی غیر مجاز"
        if self.request.user.has_perm(APP_NAME+".add_warehousesheet"):
            sw=True
        if not sw and me_employee is not None:
            sw=True

        if not sw:
            return FAILED,message,None,None

        invoice_line=InvoiceLine(person_id=self.me_person.id)
        invoice_line_item_id=0
        if 'invoice_line_item_id' in kwargs:
            invoice_line_item_id=kwargs["invoice_line_item_id"]
            invoice_line.invoice_line_item_id=invoice_line_item_id

        if 'product_id' in kwargs:
            invoice_line_item_id=kwargs["product_id"]
            invoice_line.invoice_line_item_id=invoice_line_item_id

        if 'invoice_id' in kwargs:
            if kwargs['invoice_id']>0:
                invoice_line.invoice_id=kwargs["invoice_id"]
                invoice=InvoiceRepo(request=self.request).invoice(id=kwargs["invoice_id"])
                if invoice is None:
                    message='فاکتور مورد نظر وجود ندارد.'
                    return FAILED,message,None,None
                
                if invoice.status==FinancialEventStatusEnum.APPROVED:
                    message='فاکتور تایید شده و امکان تغییر ، ویرایش و افزودن سطر وجود ندارد.'
                    return FAILED,message,None,None
                
                if invoice.status==FinancialEventStatusEnum.DELIVERED:
                    message='فاکتور تحویل شده و امکان تغییر ، ویرایش و افزودن سطر وجود ندارد.'
                    return FAILED,message,None,None
                
                if invoice.status==FinancialEventStatusEnum.FINISHED:
                    message='فاکتور نهایی شده و امکان تغییر ، ویرایش و افزودن سطر وجود ندارد.'
                    return FAILED,message,None,None
        
        if 'description' in kwargs:
            invoice_line.description=kwargs["description"]
        if 'status' in kwargs:
            invoice_line.status=kwargs["status"]
        if 'quantity' in kwargs:
            invoice_line.quantity=kwargs["quantity"]
        if 'unit_price' in kwargs:
            unit_price=kwargs["unit_price"]
            invoice_line.unit_price=unit_price

        if 'unit_name' in kwargs:
            unit_name=kwargs["unit_name"]
            invoice_line.unit_name=unit_name

        if 'save' in kwargs or kwargs["default_price"]:
            save=kwargs["save"]
            if save or kwargs["default_price"]:
                if 'coef' in kwargs:
                    coef=kwargs["coef"]
                if 'default_price' in kwargs:
                    default_price=kwargs["default_price"]
                try:
                    InvoiceLineItemUnitRepo(request=self.request).add_invoice_line_item_unit(
                        invoice_line_item_id=invoice_line_item_id,
                        coef=coef,
                        default=default_price,
                        unit_name=unit_name,
                        unit_price=unit_price,)
                except:
                    pass
        result,message,invoice_line=invoice_line.save()
        # self.add_warehouse_sheet()
        warehouse_sheet=WareHouseSheet()
        warehouse_sheet.invoice_line_id=invoice_line.id
        

        
         
        if 'warehouse_id' in kwargs:
            warehouse=WareHouseRepo(request=self.request).warehouse(pk=kwargs["warehouse_id"])
            if warehouse is not None:
                warehouse_sheet.warehouse_id=warehouse.id
 
 
        if 'invoice_id' in kwargs:
            invoice=InvoiceRepo(request=self.request).invoice(pk=kwargs["invoice_id"])
            if invoice is not None:
                warehouse_sheet.invoice_id=invoice.id


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
        
        if 'organization_unit_id' in kwargs:
            
            organization_unit=OrganizationUnitRepo(request=self.request).organization_unit(pk=kwargs["organization_unit_id"])
            if organization_unit is not None:
                warehouse_sheet.organization_unit_id=organization_unit.id
 
                 

        warehouse_sheet.person=self.me_person
        warehouse_sheet.save()
        return result,message,warehouse_sheet,invoice_line


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
 

class WareHouseSheetSignatureRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=WareHouseSheetSignature.objects.filter(id=0)
        self.me_person=PersonRepo(request=request).me
        if self.me_person is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=WareHouseSheetSignature.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "warehouse_id" in kwargs:
            warehouse_id=kwargs["warehouse_id"]
            objects=objects.filter(warehouse_id=warehouse_id) 
        if "warehouse_sheet_id" in kwargs:
            warehouse_sheet_id=kwargs["warehouse_sheet_id"]
            objects=objects.filter(warehouse_sheet_id=warehouse_sheet_id)  
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
        
    def warehouse_sheet_signature(self,*args, **kwargs):
        if "warehouse_id" in kwargs and kwargs["warehouse_id"] is not None:
            return self.objects.filter(pk=kwargs['warehouse_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_warehouse_sheet_signature(self,*args,**kwargs):
        result,message,warehouse_sheet_signature=FAILED,"",None
        
        
        if not self.request.user.has_perm(APP_NAME+".add_warehousesheetsignature"):
            message="دسترسی غیر مجاز"
            return result,message,warehouse_sheet_signature

        warehouse_sheet_signature=WareHouseSheetSignature()
        warehouse_sheet=WareHouseSheet.objects.filter(pk=kwargs["warehouse_sheet_id"]).first()
        if warehouse_sheet is None:
            message='برگه انبار درست انتخاب نشده است.'
            return result,message,None    
        me_employee=EmployeeRepo(request=self.request).me
        if me_employee is None:
            return FAILED,'شما حق امضا ندارید.',None
        warehouse_sheet_signature.employee_id=me_employee.id

            
        if 'warehouse_sheet_id' in kwargs:
            warehouse_sheet_signature.warehouse_sheet_id=kwargs["warehouse_sheet_id"]  

        if 'description' in kwargs:
            warehouse_sheet_signature.description=kwargs["description"]  


        if 'status' in kwargs:
            warehouse_sheet_signature.status=kwargs["status"]  

 
        warehouse_sheet_signature.save()
        if warehouse_sheet_signature.id is not None:
            result=SUCCEED
            message='امضای برگه انبار با موفقیت ذخیره شد.'
        return result,message,warehouse_sheet_signature
 