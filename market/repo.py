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
from authentication.repo import PersonRepo
from accounting.repo import PersonCategoryEnum


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
        if "product_id" in kwargs:
            product_id=kwargs["product_id"]
            objects=objects.filter(product_id=product_id)
        if "level" in kwargs:
            level=kwargs["level"]
            objects=objects.filter(level=level)
        if "customer_id" in kwargs:
            from .enums import Cus  
            level=ShopLevelEnum.GUEST
            customer_id=kwargs["customer_id"]
            customer=CustomerRepo(request=self.request).customer(customer_id=customer_id)
            if customer is not None:
                level=customer.level
            objects=objects.filter(level=level)
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



class CustomerRepo():
    def __init__(self,request,*args, **kwargs):
        self.request=request
        self.me=None
        self.objects=Customer.objects
        profile=ProfileRepo(request=request).me
        if profile is not None:
            self.me=self.objects.filter(person__profile_id=profile.id).first()
    def list(self,*args, **kwargs):
        objects=self.objects
        pure_code="876454453342236"
        try:
            pure_code=int(kwargs["search_for"]) 
        except:
            pass
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]

            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for) | Q(pure_code=pure_code ) )
        return objects.all()
     
    def customer(self,*args, **kwargs):
        if "customer_id" in kwargs and kwargs["customer_id"] is not None:
            return self.objects.filter(pk=kwargs['customer_id']).first()
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        if "code" in kwargs and kwargs["code"] is not None:
            return self.objects.filter(code=kwargs['code']).first()
             
        if "account_code" in kwargs and kwargs["account_code"] is not None:
            a= self.objects.filter(code=kwargs['account_code']).first() 
            if a is not None:
                return a
            else:
                try:
                    a= self.objects.filter(pure_code=filter_number(kwargs['account_code'])).first() 
                    if a is not None:
                        return a
                except:
                    pass
        
        
    def add_customer(self,*args,**kwargs):
        result,message,customer=FAILED,"",None
        me_supplier=SupplierRepo(request=self.request).me
        if not self.request.user.has_perm(APP_NAME+".add_customer") :
            message="دسترسی غیر مجاز"
            return result,message,customer
        # if len(Product.objects.filter(product_id=kwargs["product_id"]).filter(unit_name=kwargs["unit_name"]).filter(level=kwargs["level"]).filter(supplier_id=kwargs["supplier_id"]))>0:
        #     message="نام تکراری برای کالای جدید"
        #     return result,message,customer
        

        customer=Customer() 
        from accounting.repo import PersonRepo
        if kwargs['person_id']==0:
            result22,message22,person=PersonRepo(request=self.request).add_person(**kwargs)
 
            if result22==SUCCEED:
                customer.person=person
        elif 'person_id' in kwargs and kwargs['person_id'] is not None and kwargs['person_id']>0:
            customer.person_id=kwargs["person_id"]
        if 'level' in kwargs:
            customer.level=kwargs["level"]
    
        if 'code' in kwargs:
            customer.code=kwargs["code"]
             
        (result,message,customer)=customer.save() 

        return result,message,customer
 


class ShipperRepo():
    def __init__(self,request,*args, **kwargs):
        self.request=request
        self.me=None
        self.objects=Shipper.objects
        profile=ProfileRepo(request=request).me
        if profile is not None:
            self.me=self.objects.filter(person__profile_id=profile.id).first()
    def list(self,*args, **kwargs):
        objects=self.objects
        pure_code="876454453342236"
        try:
            pure_code=int(kwargs["search_for"]) 
        except:
            pass
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]

            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for) | Q(pure_code=pure_code ) )
        return objects.all()
     
    def shipper(self,*args, **kwargs):
        if "shipper_id" in kwargs and kwargs["shipper_id"] is not None:
            return self.objects.filter(pk=kwargs['shipper_id']).first()
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        if "code" in kwargs and kwargs["code"] is not None:
            return self.objects.filter(code=kwargs['code']).first()
             
        if "account_code" in kwargs and kwargs["account_code"] is not None:
            a= self.objects.filter(code=kwargs['account_code']).first() 
            if a is not None:
                return a
            else:
                try:
                    a= self.objects.filter(pure_code=filter_number(kwargs['account_code'])).first() 
                    if a is not None:
                        return a
                except:
                    pass
        
        
    def add_shipper(self,*args,**kwargs):
        result,message,shipper=FAILED,"",None
        me_supplier=SupplierRepo(request=self.request).me
        if not self.request.user.has_perm(APP_NAME+".add_shipper") :
            message="دسترسی غیر مجاز"
            return result,message,shipper
        # if len(Product.objects.filter(product_id=kwargs["product_id"]).filter(unit_name=kwargs["unit_name"]).filter(level=kwargs["level"]).filter(supplier_id=kwargs["supplier_id"]))>0:
        #     message="نام تکراری برای کالای جدید"
        #     return result,message,shipper
        

        shipper=Shipper() 
        from accounting.repo import PersonRepo
        if kwargs['person_id']==0:
            result22,message22,person=PersonRepo(request=self.request).add_person(**kwargs)
 
            if result22==SUCCEED:
                shipper.person=person
        elif 'person_id' in kwargs and kwargs['person_id'] is not None and kwargs['person_id']>0:
            shipper.person_id=kwargs["person_id"]
        if 'level' in kwargs:
            shipper.level=kwargs["level"]
    
        if 'code' in kwargs:
            shipper.code=kwargs["code"]
             
        (result,message,shipper)=shipper.save() 

        return result,message,shipper
 
 

class CartItemRepo():
    def __init__(self,request,*args, **kwargs):
        self.request=request
        self.me=None
        # profile=ProfileRepo(request=request).me
        self.objects=CartItem.objects
        # if profile is not None:
        #     self.me=self.objects.filter(profile=profile).first()
    def list(self,*args, **kwargs):
        objects=self.objects
        pure_code="876454453342236"
        try:
            pure_code=int(kwargs["search_for"]) 
        except:
            pass
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for) | Q(pure_code=pure_code ) )
            
        if "supplier_id" in kwargs:
            supplier_id=kwargs["supplier_id"]
            objects=objects.filter(supplier_id=supplier_id)

            
        if "customer_id" in kwargs:
            customer_id=kwargs["customer_id"]
            objects=objects.filter(customer_id=customer_id)

        if "product_id" in kwargs:
            product_id=kwargs["product_id"]
            objects=objects.filter(product_id=product_id)
        if "level" in kwargs:
            level=kwargs["level"]
            objects=objects.filter(level=level)
        return objects.all()
    

    def shop(self,*args, **kwargs):
        if "shop_id" in kwargs and kwargs["shop_id"] is not None:
            return self.objects.filter(pk=kwargs['shop_id']).first() 
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        if "code" in kwargs and kwargs["code"] is not None:
            return self.objects.filter(code=kwargs['code']).first()
             
        if "barcode" in kwargs and kwargs["barcode"] is not None:
            a= self.objects.filter(barcode=kwargs['barcode']).first() 
            return a 
           
    def add_to_cart(self,*args,**kwargs):
        result,message,cart_item=FAILED,"",None
        me_customer=CustomerRepo(request=self.request).me
        if  me_customer is None and not self.request.user.has_perm(APP_NAME+".add_cartitem") :
            message="دسترسی غیر مجاز"
            return result,message,cart_item
        # if len(Product.objects.filter(product_id=kwargs["product_id"]).filter(unit_name=kwargs["unit_name"]).filter(level=kwargs["level"]).filter(customer_id=kwargs["customer_id"]))>0:
        #     message="نام تکراری برای کالای جدید"
        #     return result,message,cart_item
        if me_customer is None:
            message=" 22دسترسی غیر مجاز"
            return result,message,cart_item

        cart_item=CartItem(customer_id=me_customer.id) 
        if 'shop_id' in kwargs:
            cart_item.shop_id=kwargs["shop_id"]
         
        if 'quantity' in kwargs:
            cart_item.quantity=kwargs["quantity"] 

        (result,message,cart_item)=cart_item.save() 

        return result,message,cart_item
 
 
    def checkout(self,*args,**kwargs):
        result,message,invoices=FAILED,"",[]
        me_customer=CustomerRepo(request=self.request).me
        if  me_customer is None and not self.request.user.has_perm(APP_NAME+".add_cartitem") :
            message="دسترسی غیر مجاز"
            return result,message,invoices
        # if len(Product.objects.filter(product_id=kwargs["product_id"]).filter(unit_name=kwargs["unit_name"]).filter(level=kwargs["level"]).filter(customer_id=kwargs["customer_id"]))>0:
        #     message="نام تکراری برای کالای جدید"
        #     return result,message,cart_item
        if me_customer is None:
            message=" 22دسترسی غیر مجاز"
            return result,message,invoices
        customer_id=kwargs["customer_id"]
        invoices=[]
        cart_items=CartItem.objects.filter(customer_id=customer_id)
        suppliers_ids=[]
        for cart_item in cart_items:
            supplier_id=cart_item.shop.supplier.id
            if supplier_id not in suppliers_ids:
                suppliers_ids.append(supplier_id)
        customer=CustomerRepo(request=self.request).customer(pk=customer_id)
        if customer is None:
            return FAILED,"مشتری نادرست انتخاب شده است",[]
        for supplier_id in suppliers_ids:

            supplier=SupplierRepo(request=self.request).supplier(pk=supplier_id)    
            from accounting.repo import InvoiceRepo,Invoice,InvoiceLine
            from django.utils import timezone
            invoice_data={}
            invoice_data['bedehkar_id']=customer.account.id
            invoice_data['bestankar_id']=supplier.account.id
            invoice_data['title']="فاکتور جدید"
            invoice_data['amount']=0
            invoice_data['event_datetime']=timezone.now()
            # invoice=Invoice(invoice_data)
            invoice_repo=InvoiceRepo(request=self.request)
            invoice,message,result=invoice_repo.add_invoice(**invoice_data)

            # invoice.save()
            invoices.append(invoice)
            for cart_item in cart_items:
                if cart_item.shop.supplier.id==supplier_id:
                    invoice_line=InvoiceLine()
                    invoice_line.invoice_id=invoice.id
                    invoice_line.invoice_line_item_id=cart_item.shop.product_id
                    invoice_line.quantity=cart_item.quantity
                    invoice_line.unit_price=cart_item.shop.unit_price
                    invoice_line.unit_name=cart_item.shop.unit_name
                    invoice_line.save() 
                    cart_item.delete()
        return result,message,invoices
 


class SupplierRepo():
    def __init__(self,request,*args, **kwargs):
        self.request=request
        self.me=None
        self.objects=Supplier.objects

        profile=ProfileRepo(request=request).me
        if profile is not None:
            self.me=self.objects.filter(person__profile_id=profile.id).first()

    def list(self,*args, **kwargs):
        objects=self.objects
        pure_code="876454453342236"
        try:
            pure_code=int(kwargs["search_for"]) 
        except:
            pass
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]

            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for) | Q(pure_code=pure_code ) )
        return objects.all()
    

    def supplier(self,*args, **kwargs):
        if "supplier_id" in kwargs and kwargs["supplier_id"] is not None:
            return self.objects.filter(pk=kwargs['supplier_id']).first() 
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        if "code" in kwargs and kwargs["code"] is not None:
            return self.objects.filter(code=kwargs['code']).first()
             
        if "barcode" in kwargs and kwargs["barcode"] is not None:
            a= self.objects.filter(barcode=kwargs['barcode']).first() 
            return a 
           


              
    def add_supplier(self,*args,**kwargs):
        result,message,supplier=FAILED,"",None
        me_supplier=SupplierRepo(request=self.request).me
        if not self.request.user.has_perm(APP_NAME+".add_supplier") :
            message="دسترسی غیر مجاز"
            return result,message,supplier
        # if len(Product.objects.filter(product_id=kwargs["product_id"]).filter(unit_name=kwargs["unit_name"]).filter(level=kwargs["level"]).filter(supplier_id=kwargs["supplier_id"]))>0:
        #     message="نام تکراری برای کالای جدید"
        #     return result,message,supplier
        

        supplier=Supplier() 
        if kwargs['person_id']==0:
            result22,message22,person=PersonRepo(request=self.request).add_person(**kwargs)
            supplier.person=person
 
            if person is not None:
                from accounting.repo import PersonAccountRepo,PersonCategoryRepo
                p_c=PersonCategoryRepo(request=self.request).person_category(title=PersonCategoryEnum.SUPPLIER)
                result,message,supplier_account=PersonAccountRepo(request=self.request).add_person_account(person_id=person.id,person_category_id=p_c.id)
             
                supplier.account=supplier_account
        elif 'person_id' in kwargs and kwargs['person_id'] is not None and kwargs['person_id']>0:
            person_id=kwargs["person_id"]
            person=PersonRepo(request=self.request).person(person_id=person_id)
            if person is not None:
                supplier.person=person
                person_accounts=person.personaccount_set.all()
                supplier_account=person_accounts.filter(person_category__title=PersonCategoryEnum.SUPPLIER).first()
                if supplier_account is None:
                    from accounting.repo import PersonAccountRepo,PersonCategoryRepo
                    person_category=PersonCategoryRepo(request=self.request).person_category(title=PersonCategoryEnum.SUPPLIER)
                    result,message,supplier_account=PersonAccountRepo(request=self.request).add_person_account(person_id=person.id,person_category_id=person_category.id)
                from accounting.models import PersonAccount
                supplier.account_id=supplier_account.id
            supplier.person_id=person.id

        if 'level' in kwargs:
            supplier.level=kwargs["level"] 
              
        (result,message,supplier)=supplier.save() 
        return result,message,supplier
  