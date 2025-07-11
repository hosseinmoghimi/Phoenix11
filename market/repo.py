from .models import Shop,Supplier,Customer,CartItem,Shipper,Menu,Desk,DeskCustomer

from .apps import APP_NAME
from .enums import *
from log.repo import LogRepo 
from django.db.models import Q
from django.shortcuts import reverse
from authentication.repo import ProfileRepo
from accounting.repo import InvoiceLineItemUnitRepo
from utility.num import filter_number
from utility.calendar import PersianCalendar
from utility.constants import FAILED,SUCCEED
from utility.log import leolog


class MenuRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Menu.objects.filter(id=0)
        profile=ProfileRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_menu"):
                self.objects=Menu.objects
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
        
    def menu(self,*args, **kwargs):
        if "menu_id" in kwargs and kwargs["menu_id"] is not None:
            return self.objects.filter(pk=kwargs['menu_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_menu(self,*args,**kwargs):
        result,message,menu=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_menu"):
            message="دسترسی غیر مجاز"
            return result,message,menu

        menu=Menu()
        if 'title' in kwargs:
            menu.title=kwargs["title"]
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                menu.parent_id=kwargs["parent_id"]
        if 'color' in kwargs:
            menu.color=kwargs["color"]
        if 'supplier_id' in kwargs:
            menu.supplier_id=kwargs["supplier_id"]
        if 'priority' in kwargs:
            menu.priority=kwargs["priority"]
        if 'type' in kwargs:
            menu.type=kwargs["type"]

            
        

        if 'nature' in kwargs:
            menu.nature=kwargs["nature"]
        (result,message,menu)=menu.save()
        return result,message,menu


 
class SupplierRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Supplier.objects.filter(id=0)
        profile=ProfileRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_supplier"):
                self.objects=Supplier.objects
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
        
    def supplier(self,*args, **kwargs):
        if "supplier_id" in kwargs and kwargs["supplier_id"] is not None:
            return self.objects.filter(pk=kwargs['supplier_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_supplier(self,*args,**kwargs):
        result,message,supplier=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_supplier"):
            message="دسترسی غیر مجاز"
            return result,message,supplier

        supplier=Supplier()
        if 'title' in kwargs:
            supplier.title=kwargs["title"]
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                supplier.parent_id=kwargs["parent_id"]
        if 'color' in kwargs:
            supplier.color=kwargs["color"]
        if 'supplier_id' in kwargs:
            supplier.supplier_id=kwargs["supplier_id"]
        if 'priority' in kwargs:
            supplier.priority=kwargs["priority"]
        if 'type' in kwargs:
            supplier.type=kwargs["type"]

            
        if 'parent_code' in kwargs:
            parent_code= kwargs["parent_code"]
            parent=Account.objects.filter(code=parent_code).first()
            if parent is not None:
                supplier.parent_id=parent.id

        if 'nature' in kwargs:
            supplier.nature=kwargs["nature"]
        (result,message,supplier)=supplier.save()
        return result,message,supplier


 

class DeskRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Desk.objects.filter(id=0)
        profile=ProfileRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_desk"):
                self.objects=Desk.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        if "supplier_id" in kwargs:
            supplier_id=kwargs["supplier_id"]
            objects=objects.filter(supplier_id=supplier_id)  
        return objects.all()
        
    def desk(self,*args, **kwargs):
        if "desk_id" in kwargs and kwargs["desk_id"] is not None:
            return self.objects.filter(pk=kwargs['desk_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_desk(self,*args,**kwargs):
        result,message,desk=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_desk"):
            message="دسترسی غیر مجاز"
            return result,message,desk

        desk=Desk()
        if 'title' in kwargs:
            desk.title=kwargs["title"]
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                desk.parent_id=kwargs["parent_id"]
        if 'color' in kwargs:
            desk.color=kwargs["color"]
        if 'supplier_id' in kwargs:
            desk.supplier_id=kwargs["supplier_id"]
        if 'priority' in kwargs:
            desk.priority=kwargs["priority"]
        if 'type' in kwargs:
            desk.type=kwargs["type"]

            
        if 'parent_code' in kwargs:
            parent_code= kwargs["parent_code"]
            parent=Account.objects.filter(code=parent_code).first()
            if parent is not None:
                desk.parent_id=parent.id

        if 'nature' in kwargs:
            desk.nature=kwargs["nature"]
        (result,message,desk)=desk.save()
        return result,message,desk


class DeskCustomerRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=DeskCustomer.objects.filter(id=0)
        profile=ProfileRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_desk_customer"):
                self.objects=DeskCustomer.objects
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
        
    def desk_customer(self,*args, **kwargs):
        if "desk_customer_id" in kwargs and kwargs["desk_customer_id"] is not None:
            return self.objects.filter(pk=kwargs['desk_customer_id']).first()  
        if "desk_id" in kwargs and kwargs["desk_id"] is not None:
            return self.objects.filter(desk_id=kwargs['desk_id']).first()  
        
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_desk_customer(self,*args,**kwargs):
        result,message,desk_customer=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_desk_customer"):
            message="دسترسی غیر مجاز"
            return result,message,desk_customer

        desk_customer=DeskCustomer()
        if 'title' in kwargs:
            desk_customer.title=kwargs["title"]
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                desk_customer.parent_id=kwargs["parent_id"]
        if 'color' in kwargs:
            desk_customer.color=kwargs["color"]
        if 'supplier_id' in kwargs:
            desk_customer.supplier_id=kwargs["supplier_id"]
        if 'priority' in kwargs:
            desk_customer.priority=kwargs["priority"]
        if 'type' in kwargs:
            desk_customer.type=kwargs["type"]

            
        if 'parent_code' in kwargs:
            parent_code= kwargs["parent_code"]
            parent=Account.objects.filter(code=parent_code).first()
            if parent is not None:
                desk_customer.parent_id=parent.id

        if 'nature' in kwargs:
            desk_customer.nature=kwargs["nature"]
        (result,message,desk_customer)=desk_customer.save()
        return result,message,desk_customer


class ShopRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Shop.objects.filter(id=0)
        profile=ProfileRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_desk"):
                self.objects=Shop.objects
                self.my_accounts=self.objects 
    def primary_shop(self,product,*args, **kwargs):
        if product is None :
            return None
        shops=Shop.objects.filter(product_id=product.id)
        if len(shops)==1:
            return shops.first()
        return None
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        if "supplier_id" in kwargs:
            supplier_id=kwargs["supplier_id"]
            objects=objects.filter(supplier_id=supplier_id)  
        return objects.all()
        
    def shop(self,*args, **kwargs):
        if "shop_id" in kwargs and kwargs["shop_id"] is not None:
            return self.objects.filter(pk=kwargs['shop_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_shop(self,*args,**kwargs):
        result,message,shop=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_shop"):
            message="دسترسی غیر مجاز"
            return result,message,shop

        shop=Shop()
        if 'title' in kwargs:
            shop.title=kwargs["title"]
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                shop.parent_id=kwargs["parent_id"]
        if 'color' in kwargs:
            shop.color=kwargs["color"]
        if 'supplier_id' in kwargs:
            shop.supplier_id=kwargs["supplier_id"]
        if 'priority' in kwargs:
            shop.priority=kwargs["priority"]
        if 'type' in kwargs:
            shop.type=kwargs["type"]

         
        (result,message,shop)=shop.save()
        return result,message,shop

