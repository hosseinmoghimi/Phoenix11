from .models import InvoiceLineItemUnit,InvoiceLineItem,Account,Product,Service,FinancialEvent,Invoice,Bank,BankAccount,PersonCategory,Person,AccountingDocument,AccountingDocumentLine,FinancialYear,PersonAccount
from .apps import APP_NAME
from .enums import *
from log.repo import LogRepo
from django.db.models import Q
from django.shortcuts import reverse
from authentication.repo import ProfileRepo
# from processmanagement.permission import Permission,OperationEnum
from utility.num import filter_number
from utility.calendar import PersianCalendar
from utility.constants import FAILED,SUCCEED
from utility.log import leolog
from .defaults import default_accounts,default_persons,default_banks
from .enums import AccountTypeEnum,AccountNatureEnum
from .settings_on_server import ACCOUNT_LEVEL_NAMES
# from processmanagement.models import Permission
class InvoiceLineItemUnitRepo:
    def __init__(self,request,*args, **kwargs):
        self.request=request
        self.me=None
        # profile=ProfileRepo(request=request).me
        
        
        self.objects=None
        if request.user.has_perm(APP_NAME+".view_event"):
            self.objects=InvoiceLineItemUnit.objects
        elif request.user.is_authenticated:
            accs=[]
            for person in Person.objects.filter(profile__user_id=request.user.id):

                my_accounts=AccountRepo(request=request).my_accounts
                for acc in my_accounts:
                    accs.append(acc.id)
            self.objects=Event.objects.filter(Q(bedehkar_id__in=accs)|Q(bestankar_id__in=accs))
        else:
            self.objects=Event.objects.filter(pk=0)

    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for']) 
        return objects.all()
    def product_unit(self,*args, **kwargs):
        if "product_unit_id" in kwargs:
            return self.objects.filter(pk=kwargs['product_unit_id']).first() 
        if "pk" in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs:
            return self.objects.filter(pk=kwargs['id']).first() 

                     
    def add_invoice_line_item_unit(self,*args, **kwargs):
        invoice_line_item_unit,message,result=(None,"",FAILED)
        # if not Permission(request=self.request).is_permitted(APP_NAME,OperationEnum.ADD,"productprice"):
        if not self.request.user.has_perm(APP_NAME+".add_invoicelineitemunit"):
            message="دسترسی غیر مجاز"
            return result,message,invoice_line_item_unit
        
 
        invoice_line_item_unit=InvoiceLineItemUnit()
        if 'invoice_line_item_id' in kwargs:
            invoice_line_item_unit.invoice_line_item_id=kwargs['invoice_line_item_id']

        if 'service' in kwargs:
            invoice_line_item_unit.invoice_line_item_id=kwargs['service']
        
        if 'product_id' in kwargs:
            invoice_line_item_unit.invoice_line_item_id=kwargs['product_id']
        if 'unit_price' in kwargs:
            invoice_line_item_unit.unit_price=kwargs['unit_price']
        if 'unit_name' in kwargs:
            invoice_line_item_unit.unit_name=kwargs['unit_name']
        if 'default' in kwargs:
            invoice_line_item_unit.default=kwargs['default']
        if 'coef' in kwargs:
            invoice_line_item_unit.coef=kwargs['coef']
        if invoice_line_item_unit.unit_price<1:
            message='قیمت را صفر انتخاب کرده اید.'
            return result,message,invoice_line_item_unit
        invoice_line_item_unit.save()
        result=SUCCEED
        message="قیمت جدید با موفقیت اضافه گردید."
         
 
        return result,message,invoice_line_item_unit



class AccountRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Account.objects.filter(id=0)
        profile=ProfileRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=Account.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            codeee=str(filter_number(search_for))
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for) | Q(code=codeee) )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        if "level" in kwargs:
            level=kwargs["level"]
            objects=objects.filter(level=level)  
        return objects.all()
       
    def roots(self,*args, **kwargs):
        objects=self.objects.filter(parent_id=None)
        return objects.all()

    def account(self,*args, **kwargs):
        if "account_id" in kwargs and kwargs["account_id"] is not None:
            return self.objects.filter(pk=kwargs['account_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        if "code" in kwargs and kwargs["code"] is not None:
            code=kwargs['code']
            code=kwargs['code']

            account= self.objects.filter(code=code).first()
            return account
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
          
    def set_priority(self,*args, **kwargs):
        result,message,priority=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".change_account"):
            return result,message,account_tags
        priority=kwargs['priority']
        account_id=kwargs['account_id']
        account=Account.objects.filter(pk=account_id).first()
        if account is not None:
            account.priority=priority
            account.save()
        result=SUCCEED
        return result,message,priority

           
    def set_account_parent(self,*args, **kwargs):
        result,message,account,parent=FAILED,"",None,None
        account=self.account(*args,**kwargs)
        parent=None
        parent_code=kwargs["parent_code"]
        parent=self.account(account_code=parent_code)
        account.parent=parent
        account.save()
        result=SUCCEED
        message="با موفقیت تغییر یافت"
        return result,message,account,parent


    def initial_default_accounts(self,*args, **kwargs):
        account_group_counter=0
        basic_accounts_counter=0
        moein_accounts_counter=0
        moein2_accounts_counter=0
        tafsili_accounts_counter=0 

        result=SUCCEED
        message=""  
        if not self.request.user.has_perm(APP_NAME+".add_account"):
            message="دسترسی غیر مجاز"
            result=FAILED
            return message,result
        
        accounts=default_accounts() 

        for account in accounts:
            parent_account=None
            if 'parent_code' in account:
                parent_account=Account.objects.filter(code=account["parent_code"]).first()
            new_account=Account(name=account["name"],color=account["color"],code=account['code'],priority=account['priority'],parent=parent_account)
            # new_account=Account(parent=parent_account,**kwargs)
            new_account.save()
            # account_group_counter+=1
            # basic_accounts_counter+=1   
 
                                  
        accounts=Account.objects
        account_group_counter=len(accounts.filter(type=AccountTypeEnum.GROUP))
        basic_accounts_counter=len(accounts.filter(type=AccountTypeEnum.BASIC))
        moein_accounts_counter=len(accounts.filter(type=AccountTypeEnum.MOEIN_1))
        moein2_accounts_counter=len(accounts.filter(type=AccountTypeEnum.MOEIN_2))
        tafsili_accounts_counter=len(accounts.filter(Q(type=AccountTypeEnum.TAFSILI_1)|Q(type=AccountTypeEnum.TAFSILI_2)|Q(type=AccountTypeEnum.TAFSILI_3)|Q(type=AccountTypeEnum.TAFSILI_4)))
                                                        

        if result==SUCCEED:
            message="با موفقیت اضافه گردید."
        message+=f"<br>{account_group_counter}   گروه حساب" 
        message+=f"<br>{basic_accounts_counter}   حساب  کل " 
        message+=f"<br>{moein_accounts_counter}  حساب معین سطح یک " 
        message+=f"<br>{moein2_accounts_counter}  حساب معین سطح دو " 
        message+=f"<br>{tafsili_accounts_counter}  حساب تفصیلی " 

        me_profile=ProfileRepo(request=self.request).me
        new_log={}
        new_log['title']="افزودن حساب های پیش فرض"
        new_log['app_name']=APP_NAME
        new_log['profile']=me_profile
        new_log['description']="حساب های پیش فرض اضافه شدند."
        LogRepo(request=self.request).add_log(**new_log)
        return result,message
 
    def delete_all_accounts(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".delete_account"):
            message="دسترسی غیر مجاز"
            return message,result
        AccountingDocumentLine.objects.all().delete()
        FinancialEvent.objects.all().delete()
        AccountingDocument.objects.all().delete()
        # TafsiliAccount.objects.all().delete()
        # MoeinAccount.objects.all().delete()
        # BasicAccount.objects.all().delete()
        # AccountGroup.objects.all().delete() 
        Account.objects.all().delete() 
        result=SUCCEED
        message="همه حساب ها حذف شد."

        me_profile=ProfileRepo(request=self.request).me
        new_log={}
        new_log['title']="حذف همه حساب ها"
        new_log['app_name']=APP_NAME
        new_log['profile']=me_profile
        new_log['description']="همه ی حساب ها حذف شدند."
        LogRepo(request=self.request).add_log(**new_log)

        return result,message
    
    def set_priority(self,*args, **kwargs):
        result,message,priority=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".change_account"):
            return result,message,account_tags
        priority=kwargs['priority']
        account_id=kwargs['account_id']
        
         

        account=Account.objects.filter(pk=account_id).first()
        if account is not None:
            account.priority=priority
            account.save()

        result=SUCCEED

        return result,message,priority

    def add_account(self,*args,**kwargs):
        result,message,account=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_account"):
            message="دسترسی غیر مجاز"
            return result,message,account

        account=Account()
        if 'name' in kwargs:
            account.name=kwargs["name"]
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                account.parent_id=kwargs["parent_id"]
        if 'color' in kwargs:
            account.color=kwargs["color"]
        if 'code' in kwargs:
            account.code=kwargs["code"]
        if 'priority' in kwargs:
            account.priority=kwargs["priority"]
        if 'type' in kwargs:
            account.type=kwargs["type"]

            
        if 'parent_code' in kwargs:
            parent_code= kwargs["parent_code"]
            parent=Account.objects.filter(code=parent_code).first()
            if parent is not None:
                account.parent_id=parent.id

        if 'nature' in kwargs:
            account.nature=kwargs["nature"]
        (result,message,account)=account.save()
        return result,message,account


class PersonAccountRepo():
    def __init__(self,request,*args, **kwargs):
        self.request=request
        self.me=None
        # profile=ProfileRepo(request=request).me
        self.objects=PersonAccount.objects 
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

            objects=objects.filter(Q(category__contains=search_for)   )

        if "category" in kwargs:
            category=kwargs["category"]
            objects=objects.filter(Q(category=category)   )
        return objects.all()
  
    def add_person_account(self,*args, **kwargs):
        result,message,person_account=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_personaccount"):
            message="دسترسی غیر مجاز"
            return result,message,person_account
        person_account=PersonAccount()
        if 'person' in kwargs:
            person_account.person=kwargs['person']
        if 'person_id' in kwargs:
            person_account.person_id=kwargs['person_id']
        if 'person_category' in kwargs:
            person_account.person_category=kwargs['person_category']
        if 'person_category_id' in kwargs:
            person_account.person_category_id=kwargs['person_category_id']
        person_account.save()
        result=SUCCEED
        message="با موفقیت حساب فرد ایجاد شد."
        return result,message,person_account

    def person_account(self,*args, **kwargs):
        if "person_account_id" in kwargs and kwargs["person_account"] is not None:
            return self.objects.filter(pk=kwargs['person_account_id']).first() 
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
                    
    def delete_all(self,*args,**kwargs):
        
        if not self.request.user.has_perm(APP_NAME+".delete_personaccount"):
            message="دسترسی غیر مجاز"
            return result,message
        PersonAccount.objects.all().delete() 
                   
        result=SUCCEED
        message="همه حذف شدند."
        return result,message
     

class FinancialYearRepo():
    def __init__(self,request,*args, **kwargs):
        self.request=request
        self.me=None
        # profile=ProfileRepo(request=request).me
        self.objects=FinancialYear.objects

        
        self.objects=None
        if request.user.has_perm(APP_NAME+".view_person"):
            self.objects=FinancialYear.objects
        elif request.user.is_authenticated:
            self.objects=FinancialYear.objects.filter(profile__user_id=request.user.id)
                 
        else:
            self.objects=Person.objects.filter(pk=0)

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
        return objects.all()
     
    def financial_year(self,*args, **kwargs):
        if "financial_year_id" in kwargs and kwargs["financial_year_id"] is not None:
            return self.objects.filter(pk=kwargs['financial_year_id']).first()
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        if "date" in kwargs and kwargs["date"] is not None:
            return self.objects.filter(start_date_lte=kwargs['date']).filter(end_date_gte=kwargs['date']).first() 
        
   
   
    def add_financial_year(self,*args,**kwargs):
        result,message,financial_year,financial_years=FAILED,"",None,[]
        if not self.request.user.has_perm(APP_NAME+".add_financialyear"):
            message="دسترسی غیر مجاز"
            return result,message,financial_year,financial_years

        financial_year=FinancialYear() 

 

    
        if 'start_date' in kwargs:
            year=kwargs['start_date'][:2]
            if year=="13" or year=="14":
                kwargs['start_date']=PersianCalendar().to_gregorian(kwargs["start_date"])
            financial_year.start_date=kwargs['start_date']

            
        if 'end_date' in kwargs:
            year=kwargs['end_date'][:2]
            if year=="13" or year=="14":
                kwargs['end_date']=PersianCalendar().to_gregorian(kwargs["end_date"])
            financial_year.end_date=kwargs['end_date']

 

        if 'name' in kwargs:
            financial_year.name=kwargs["name"] 

        if 'description' in kwargs:
            financial_year.description=kwargs["description"] 

        if 'status' in kwargs:
            financial_year.status=kwargs["status"] 
 
        if(len(FinancialYear.objects.filter(name=financial_year.name))>0):
            financial_year=None
            message="نام وارد شده تکراری است."
            result=FAILED
            return result,message,financial_year,financial_years

 
        (result,message,financial_year)=financial_year.save()
        if result==FAILED:
            return result,message,financial_year,financial_years
        
        financial_years=FinancialYear.objects.order_by("start_date")
 
        return result,message,financial_year,financial_years
 
      
class PersonCategoryRepo():
    def __init__(self,request,*args, **kwargs):
        self.request=request
        self.me=None
        # profile=ProfileRepo(request=request).me
        self.objects=PersonCategory.objects
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
        return objects.all()
     

     
    def delete_all(self,*args,**kwargs):
        
        if not self.request.user.has_perm(APP_NAME+".delete_personcategory"):
            message="دسترسی غیر مجاز"
            return result,message,person
        PersonCategory.objects.all().delete()
        
        result=SUCCEED
        message="همه حذف شدند."
        return result,message

    def person_category(self,*args, **kwargs):
        if "person_id" in kwargs and kwargs["person_id"] is not None:
            return self.objects.filter(pk=kwargs['person_id']).first()
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        if "code" in kwargs and kwargs["code"] is not None:
            return self.objects.filter(code=kwargs['code']).first()
        if "title" in kwargs and kwargs["title"] is not None:
            return self.objects.filter(title=kwargs['title']).first()
             
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
       
    def add_person_category(self,*args,**kwargs):
        result,message,person_category=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_personcategory"):
            message="دسترسی غیر مجاز"
            return result,message,person_category
         
        person_category=PersonCategory()
          
        if 'account_code' in kwargs:
            account_code=kwargs["account_code"]
            person_category.account=Account.objects.filter(code=account_code).first()

          
         
        if 'title' in kwargs:
            if len(PersonCategory.objects.filter(title=kwargs["title"]))>0:
                message="نام وارد شده تکراری می باشد."
                return result,message,None
            person_category.title=kwargs["title"]
        if 'priority' in kwargs:
            person_category.priority=kwargs["priority"] 
        person_category.save()
        result=SUCCEED
        message="دسته بندی جدید برای اشخاص با موفقیت اضافه گردید."
        # (result,message,person_category)=person_category.save()
        # (result,message,person_category)=person_category.save()
        return result,message,person_category

    def initial_default_person_categories(self,*args,**kwargs):
        result=SUCCEED
        message=""
        person_categories,persons=default_persons()
        for person_category in person_categories:
            result,message,new_person_category=self.add_person_category(**person_category)
                
        for person in persons:
            result,message,new_person=PersonRepo(request=self.request).add_person(**person)

        return result,message       


class ProductRepo():
    def __init__(self,request,*args, **kwargs):
        self.request=request
        self.me=None
        # profile=ProfileRepo(request=request).me
        self.objects=Product.objects
        # if profile is not None:
        #     self.me=self.objects.filter(profile=profile).first()
    def list(self,*args, **kwargs):
        objects=self.objects
        
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]

            objects=objects.filter(Q(title__contains=search_for))
        return objects.all()
    
    def add_product_to_category(self,*args, **kwargs):
        
        result,message,category,product_categories=FAILED,"",None,[]
        if not self.request.user.has_perm(APP_NAME+".change_product"):
            message="دسترسی غیر مجاز"
            return result,message,category,product_categories
        

        product=Product.objects.filter(pk=kwargs['product_id']).first()
        category=Category.objects.filter(pk=kwargs['category_id']).first()
        if category is not None and product is not None:
            if product in category.products.all():
                category.products.remove(product.id)
                message="حذف شد"
            else:
                category.products.add(product.id)
                message="اضافه شد"
            result=SUCCEED
            product_categories=product.category_set.all()
        return result,message,category,product_categories
       
    def product(self,*args, **kwargs):
        if "product_id" in kwargs and kwargs["product_id"] is not None:
            return self.objects.filter(pk=kwargs['product_id']).first() 
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        if "code" in kwargs and kwargs["code"] is not None:
            return self.objects.filter(barcode=kwargs['code']).first()
             
        if "barcode" in kwargs and kwargs["barcode"] is not None:
            a= self.objects.filter(barcode=kwargs['barcode']).first() 
            return a 
           
    def add_product(self,*args,**kwargs):
        result,message,product=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_product"):
            message="دسترسی غیر مجاز"
            return result,message,product
        if len(Product.objects.filter(title=kwargs["title"]))>0:
            message="نام تکراری برای کالای جدید"
            return result,message,product

        product=Product() 

        if 'title' in kwargs:
            product.title=kwargs["title"]
         
        if 'barcode' in kwargs and kwargs["barcode"] is not None and not kwargs["barcode"]=="":
            product.barcode=kwargs["barcode"]
        
        if product.barcode is not None and len(product.barcode)>0:
            
            if len(Product.objects.filter(barcode=product.barcode))>0:
                message="بارکد تکراری برای کالای جدید"
                return result,message,None

        (result,message,product)=product.save()
        leolog(kwargs=kwargs)
        if 'unit_price' in kwargs:
            if 'unit_name' in kwargs:
                if 'coef' in kwargs:
                    ili_unit=InvoiceLineItemUnit()
                    ili_unit.unit_name=kwargs["unit_name"]
                    ili_unit.coef=kwargs["coef"]
                    ili_unit.unit_price=kwargs["unit_price"]
                    ili_unit.invoice_line_item_id=product.id
                    ili_unit.default=True
                    ili_unit.save()
                    leolog(ili_unit=ili_unit)

                 

        if 'category_id' in kwargs:
            pass
            # category_id=kwargs["category_id"]
            # category=Category.objects.filter(pk=category_id).first()
            # if category is not None:
            #     category.products.add(product.id)
        coef=1 
        return result,message,product
 

    def import_products_from_excel(self,*args,**kwargs):
        result,message,products=FAILED,"",[]
        excel_file=kwargs['excel_file']
        # import pandas
        
        # df = pandas.read_excel(excel_file)
        # products=[]
        # for row in df.columns[0]:
        #     print (df.columns)
        import openpyxl 

        wb = openpyxl.load_workbook(excel_file)
        ws = wb.active
        count=kwargs['count']
        products_to_import=[]

        for i in range(2,count+2):
            product={}
            product['id']=ws['A'+str(i)].value
            product['title']=ws['B'+str(i)].value
            product['code']=ws['C'+str(i)].value
            product['unit_name']=ws['D'+str(i)].value
            product['unit_price']=ws['E'+str(i)].value
            product['thumbnail_origin']=ws['F'+str(i)].value
            # product['thumbnail_origin']=ws['F'+str(i)].value
            if product['title'] is not None and not product['title']=="":
                products_to_import.append(product) 
        modified=added=0
        for product in products_to_import:
            old_product=Product.objects.filter(title=product["title"]).filter(code=product["code"]).first()
            if old_product is not None:
                old_product.title=product["title"]
                old_product.unit_name=product["unit_name"]
                old_product.thumbnail_origin=product["thumbnail_origin"]
                old_product.unit_price=product["unit_price"] 
                # old_product.thumbnail_origin=product["thumbnail_origin"] 
                old_product.save()
                modified+=1
            else:
                new_product=Product()
                new_product.title=product["title"]
                new_product.barcode=product["code"]
                new_product.unit_name=product["unit_name"]
                new_product.unit_price=product["unit_price"] 
                new_product.save()
                added+=1
        result=SUCCEED
        message=f"""{added} محصول اضافه شد.
                    <br>
                    {modified} محصول ویرایش شد. """

        return result,message,products



class InvoiceLineItemRepo():
    def __init__(self,request,*args, **kwargs):
        self.request=request
        self.me=None
        # profile=ProfileRepo(request=request).me
        self.objects=InvoiceLineItem.objects
        # if profile is not None:
        #     self.me=self.objects.filter(profile=profile).first()
    def list(self,*args, **kwargs):
        objects=self.objects
        
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]

            objects=objects.filter(Q(title__contains=search_for))
        return objects.all()
    
         
    def invoice_line_item(self,*args, **kwargs):
        if "invoice_line_item_id" in kwargs and kwargs["invoice_line_item_id"] is not None:
            return self.objects.filter(pk=kwargs['invoice_line_item_id']).first() 
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        if "code" in kwargs and kwargs["code"] is not None:
            return self.objects.filter(barcode=kwargs['code']).first()
             
        if "barcode" in kwargs and kwargs["barcode"] is not None:
            a= self.objects.filter(barcode=kwargs['barcode']).first() 
            return a 
           
    def add_invoice_line_item(self,*args,**kwargs):
        result,message,invoice_line_item=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_invoice_line_item"):
            message="دسترسی غیر مجاز"
            return result,message,invoice_line_item
        if len(InvoiceLineItem.objects.filter(title=kwargs["title"]))>0:
            message="نام تکراری برای مورد جدید"
            return result,message,invoice_line_item

        invoice_line_item=InvoiceLineItem() 

        if 'title' in kwargs:
            invoice_line_item.title=kwargs["title"]
        if 'unit_price' in kwargs:
            invoice_line_item.unit_price=kwargs["unit_price"]
        if 'unit_price' in kwargs:
            invoice_line_item.unit_price=kwargs["unit_price"]
            
        if 'barcode' in kwargs and kwargs["barcode"] is not None and not kwargs["barcode"]=="":
            invoice_line_item.barcode=kwargs["barcode"]
        
        if 'unit_name' in kwargs:
            invoice_line_item.unit_name=kwargs["unit_name"]

            
        if invoice_line_item.barcode is not None and len(invoice_line_item.barcode)>0:
            
            if len(Product.objects.filter(barcode=invoice_line_item.barcode))>0:
                message="بارکد تکراری برای کالای جدید"
                return result,message,None

        (result,message,invoice_line_item)=invoice_line_item.save()
        if 'category_id' in kwargs:
            category_id=kwargs["category_id"]
            category=Category.objects.filter(pk=category_id).first()
            if category is not None:
                category.invoice_line_items.add(invoice_line_item.id)
        coef=1
        if 'coef' in kwargs:
            coef=kwargs["coef"]
        if invoice_line_item.unit_price>0:
            InvoiceLineItemUnitRepo(request=self.request).add_invoice_line_item_unit(invoice_line_item_id=invoice_line_item.id,unit_price=invoice_line_item.unit_price,unit_name=invoice_line_item.unit_name,coef=coef)
        return result,message,invoice_line_item
 

    def import_products_from_excel(self,*args,**kwargs):
        result,message,products=FAILED,"",[]
        excel_file=kwargs['excel_file']
        # import pandas
        
        # df = pandas.read_excel(excel_file)
        # products=[]
        # for row in df.columns[0]:
        #     print (df.columns)
        import openpyxl 

        wb = openpyxl.load_workbook(excel_file)
        ws = wb.active
        count=kwargs['count']
        products_to_import=[]

        for i in range(2,count+2):
            product={}
            product['id']=ws['A'+str(i)].value
            product['title']=ws['B'+str(i)].value
            product['code']=ws['C'+str(i)].value
            product['unit_name']=ws['D'+str(i)].value
            product['unit_price']=ws['E'+str(i)].value
            product['thumbnail_origin']=ws['F'+str(i)].value
            # product['thumbnail_origin']=ws['F'+str(i)].value
            if product['title'] is not None and not product['title']=="":
                products_to_import.append(product) 
        modified=added=0
        for product in products_to_import:
            old_product=Product.objects.filter(title=product["title"]).filter(code=product["code"]).first()
            if old_product is not None:
                old_product.title=product["title"]
                old_product.unit_name=product["unit_name"]
                old_product.thumbnail_origin=product["thumbnail_origin"]
                old_product.unit_price=product["unit_price"] 
                # old_product.thumbnail_origin=product["thumbnail_origin"] 
                old_product.save()
                modified+=1
            else:
                new_product=Product()
                new_product.title=product["title"]
                new_product.barcode=product["code"]
                new_product.unit_name=product["unit_name"]
                new_product.unit_price=product["unit_price"] 
                new_product.save()
                added+=1
        result=SUCCEED
        message=f"""{added} محصول اضافه شد.
                    <br>
                    {modified} محصول ویرایش شد. """

        return result,message,products


class BankAccountRepo():
    def __init__(self,request,*args, **kwargs):
        self.request=request
        self.me=None
        # profile=ProfileRepo(request=request).me
        self.objects=BankAccount.objects
       

        # if profile is not None:
        #     self.me=self.objects.filter(profile=profile).first()
    def list(self,*args, **kwargs):
        objects=self.objects
  
        if "bank_id" in kwargs:
            bank_id=kwargs["bank_id"]
            objects=objects.filter(Q(bank_id=bank_id))
  
        if "person_id" in kwargs:
            person_id=kwargs["person_id"]
            objects=objects.filter(Q(person_id=person_id))
       
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(full_name__contains=search_for) | Q(melli_code__contains=search_for) | Q(code=search_for))
        return objects.all()
     
    def bank_account(self,*args, **kwargs):
        if "bank_account_id" in kwargs and kwargs["bank_account_id"] is not None:
            return self.objects.filter(pk=kwargs['bank_account_id']).first()
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        if "code" in kwargs and kwargs["code"] is not None:
            return self.objects.filter(code=kwargs['code']).first()
             
    def add_bank_account(self,*args,**kwargs):
        result,message,bank_account=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_bankaccount"):
            message="دسترسی غیر مجاز"
            return result,message,bank_account

        bank_account=BankAccount() 

 

        if BankAccount.objects.filter(title=kwargs['title']).first() is not None:
            message="نام وارد شده تکراری است."
            bank_account=None
            return result,message,bank_account

        if BankAccount.objects.filter(code=kwargs['code']).first() is not None:
            message="کد وارد شده تکراری است."
            bank_account=None
            return result,message,bank_account

  
        if 'title' in kwargs:
            bank_account.title=kwargs["title"] 
            bank_account.name=kwargs["title"] 


            
  
        if 'card_no' in kwargs:
            bank_account.card_no=kwargs["card_no"] 

            
  
        if 'shaba_no' in kwargs:
            bank_account.shaba_no=kwargs["shaba_no"] 

            
  
        if 'account_no' in kwargs:
            bank_account.account_no=kwargs["account_no"] 

        if 'bank_id' in kwargs:
            bank_account.bank_id=kwargs["bank_id"] 

        if 'person_id' in kwargs:
            bank_account.person_id=kwargs["person_id"]

        if 'code' in kwargs:
            bank_account.code=kwargs["code"] 

        if 'parent_code' in kwargs:
            parent=Account.objects.filter(code=kwargs['parent_code']).first()
            bank_account.parent=parent
        
        bank_account.save() 
        if bank_account.id is not None:
            message="حساب بانکی جدید با موفقیت اضافه شد."
            result=SUCCEED
        return result,message,bank_account
    
      

class BankRepo():
    def __init__(self,request,*args, **kwargs):
        self.request=request
        self.me=None
        # profile=ProfileRepo(request=request).me
        self.objects=Bank.objects
       

        # if profile is not None:
        #     self.me=self.objects.filter(profile=profile).first()
    def list(self,*args, **kwargs):
        objects=self.objects
  
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(full_name__contains=search_for) | Q(melli_code__contains=search_for) | Q(code=search_for))
        return objects.all()
     
    def bank(self,*args, **kwargs):
        if "bank_id" in kwargs and kwargs["bank_id"] is not None:
            return self.objects.filter(pk=kwargs['bank_id']).first()
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        if "code" in kwargs and kwargs["code"] is not None:
            return self.objects.filter(code=kwargs['code']).first()
    
    def initial_default_banks(self,*args, **kwargs):
      
        banks_counter=0 

        result=SUCCEED
        message=""  
        if not self.request.user.has_perm(APP_NAME+".add_bank"):
            message="دسترسی غیر مجاز"
            result=FAILED
            return message,result
        for bank in default_banks():
            new_bank=Bank(name=bank["name"])
            # new_account=Account(parent=parent_account,**kwargs)
            new_bank.save()
            banks_counter+=1

        message=f"{banks_counter} بانک با موفقیت اضافه شد."
        return result,message

        
    def delete_all(self,*args, **kwargs):
      
        banks_counter=0 

        result=SUCCEED
        message=""  
        if not self.request.user.has_perm(APP_NAME+".delete_bank"):
            message="دسترسی غیر مجاز"
            result=FAILED
            return message,result
        for bank in Bank.objects.all():
            bank.delete()
            banks_counter+=1

        message=f"<p>{banks_counter} بانک با موفقیت حذف شد.</p>"
        return result,message
    
    
    def add_bank(self,*args,**kwargs):
        result,message,bank=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_bank"):
            message="دسترسی غیر مجاز"
            return result,message,bank

        bank=Bank() 

 

        if Bank.objects.filter(name=kwargs['name']).first() is not None:
            message="نام وارد شده تکراری است."
            bank=None
            return result,message,bank

  
        if 'name' in kwargs:
            bank.name=kwargs["name"] 
        bank.save()       
        message="بانک جدید با موفقیت اضافه شد."
        result=SUCCEED
        return result,message,bank

 

class ServiceRepo():
    def __init__(self,request,*args, **kwargs):
        self.request=request
        self.me=None
        # profile=ProfileRepo(request=request).me
        self.objects=Service.objects
        # if profile is not None:
        #     self.me=self.objects.filter(profile=profile).first()
    def list(self,*args, **kwargs):
        objects=self.objects
        
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]

            objects=objects.filter(Q(title__contains=search_for))
        return objects.all()
    
    def add_product_to_category(self,*args, **kwargs):
        
        result,message,category,product_categories=FAILED,"",None,[]
        if not self.request.user.has_perm(APP_NAME+".change_product"):
            message="دسترسی غیر مجاز"
            return result,message,category,product_categories
        

        product=Product.objects.filter(pk=kwargs['product_id']).first()
        category=Category.objects.filter(pk=kwargs['category_id']).first()
        if category is not None and product is not None:
            if product in category.products.all():
                category.products.remove(product.id)
                message="حذف شد"
            else:
                category.products.add(product.id)
                message="اضافه شد"
            result=SUCCEED
            product_categories=product.category_set.all()
        return result,message,category,product_categories
       
    def service(self,*args, **kwargs):
        if "service_id" in kwargs and kwargs["service_id"] is not None:
            return self.objects.filter(pk=kwargs['service_id']).first() 
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        if "code" in kwargs and kwargs["code"] is not None:
            return self.objects.filter(barcode=kwargs['code']).first()
             
        if "barcode" in kwargs and kwargs["barcode"] is not None:
            a= self.objects.filter(barcode=kwargs['barcode']).first() 
            return a 
           
    def add_service(self,*args,**kwargs):
        result,message,service=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_service"):
            message="دسترسی غیر مجاز"
            return result,message,service
        if len(Product.objects.filter(title=kwargs["title"]))>0:
            message="نام تکراری برای کالای جدید"
            return result,message,service

        service=Product() 

        if 'title' in kwargs:
            service.title=kwargs["title"]
        if 'unit_price' in kwargs:
            service.unit_price=kwargs["unit_price"]
        if 'unit_price' in kwargs:
            service.unit_price=kwargs["unit_price"]
            
        if 'barcode' in kwargs and kwargs["barcode"] is not None and not kwargs["barcode"]=="":
            service.barcode=kwargs["barcode"]
        
        if 'unit_name' in kwargs:
            service.unit_name=kwargs["unit_name"]

            
        if service.barcode is not None and len(service.barcode)>0:
            
            if len(Product.objects.filter(barcode=service.barcode))>0:
                message="بارکد تکراری برای کالای جدید"
                return result,message,None

        (result,message,service)=service.save()
        if 'category_id' in kwargs:
            category_id=kwargs["category_id"]
            category=Category.objects.filter(pk=category_id).first()
            if category is not None:
                category.services.add(service.id)
        coef=1
        if 'coef' in kwargs:
            coef=kwargs["coef"]
        if service.unit_price>0:
            ProductUnitRepo(request=self.request).add_service_unit(service_id=service.id,unit_price=service.unit_price,unit_name=service.unit_name,coef=coef)
        return result,message,service
 

class AccountingDocumentRepo():
    def __init__(self,request,*args, **kwargs):
        self.request=request
        self.me=None
        # profile=ProfileRepo(request=request).me
        self.objects=AccountingDocument.objects
        # if profile is not None:
        #     self.me=self.objects.filter(profile=profile).first()
    def list(self,*args, **kwargs):
        objects=self.objects
        if "financial_year_id" in kwargs:
            objects=objects.filter(financial_year_id=kwargs['financial_year_id']) 
        if "search_for" in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for']) 
        return objects.all()
    def accounting_document(self,*args, **kwargs):
        if "accounting_document_id" in kwargs:
            return self.objects.filter(pk=kwargs['accounting_document_id']).first() 
        if "pk" in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs:
            return self.objects.filter(pk=kwargs['id']).first() 

            
    def add_accounting_document(self,*args, **kwargs):
        result,message,accounting_document=FAILED,"",None
        if not Permission(request=self.request).is_permitted(APP_NAME,OperationEnum.ADD,"accountingdocument"):
        # if not self.request.user.has_perm(APP_NAME+".add_account"):.
            message="دسترسی غیر مجاز"
            return result,message,accounting_document
        
        f_year=FinancialYear.objects.filter(status=FinancialYearStatusEnum.IN_PROGRESS).first()
        if f_year is None:
            url=reverse(APP_NAME+":financial_years")
            message="سال مالی فعال وجود ندارد. ابتدا ایجاد کنید."+"<br>"+"<a href='"+url+"'>سال های مالی</a>"
            return result,message,accounting_document

        accounting_document=AccountingDocument(financial_year_id=f_year.id)

        if 'title' in kwargs:
            accounting_document.title=kwargs['title']
        if 'profile_id' in kwargs:
            accounting_document.profile_id=kwargs['profile_id']
        if 'description' in kwargs:
            accounting_document.description=kwargs['description']
        if 'address' in kwargs:
            accounting_document.address=kwargs['address']
        if 'tel' in kwargs:
            accounting_document.tel=kwargs['tel']
        if 'mobile' in kwargs:
            accounting_document.mobile=kwargs['mobile']
       
        
        # if 'financial_year_id' in kwargs:
        #     payment.financial_year_id=kwargs['financial_year_id']
        # else:
        #     payment.financial_year_id=FinancialYear.get_by_date(date=payment.transaction_datetime).id
        result,message,accounting_document=accounting_document.save()
        if result==SUCCEED:
            message="با موفقیت اضافه شد."
            me_profile=ProfileRepo(request=self.request).me
            new_log={}
            new_log['title']="سند مالی جدید "+" : "+accounting_document.title
            new_log['app_name']=APP_NAME
            new_log['url']=accounting_document.get_absolute_url()
            new_log['profile']=me_profile
            new_log['description']="سند مالی جدید با موفقیت اضافه گردید."
            LogRepo(request=self.request).add_log(**new_log)
        return result,message,accounting_document

class AccountingDocumentLineRepo:
    def __init__(self,request,*args, **kwargs):
        self.request=request
        self.me=None
        # profile=ProfileRepo(request=request).me
        self.objects=AccountingDocumentLine.objects
        
    def list(self,*args, **kwargs):
        objects=self.objects
        if "start_date" in kwargs and kwargs["start_date"] is not None :
            start_date=kwargs["start_date"]
            objects=objects.filter(date_time__gte=start_date) 
        if "end_date" in kwargs and kwargs["end_date"] is not None :
            end_date=kwargs["end_date"]
            objects=objects.filter(date_time__lte=end_date) 
        if "search_for" in kwargs and kwargs["search_for"] is not None and len(kwargs["search_for"])>0 :
            objects=objects.filter(Q(title__contains=kwargs['search_for'])|Q(event__title__contains=kwargs['search_for']) )
        if "amount" in kwargs and kwargs["amount"] is not None and kwargs["amount"]>0 :
            objects=objects.filter(Q(bedehkar=kwargs['amount']) | Q(bestankar=kwargs['amount']) )

            
        if "bestankar" in kwargs and kwargs["bestankar"] is not None:
            objects=objects.filter(Q(bestankar=kwargs['bestankar']) )

        if "bedehkar" in kwargs and kwargs["bedehkar"] is not None:
            objects=objects.filter(Q(bedehkar=kwargs['bedehkar']) )

        if "account_code" in kwargs and kwargs["account_code"] is not None :
            account_code=kwargs["account_code"]
            account=AccountRepo(request=self.request).account(code=account_code)
            if account is not None:
                objects=objects.filter(account_id=account.id)
        if "account_id" in kwargs and kwargs["account_id"] is not None and kwargs["account_id"]>0 :
            account_id=kwargs["account_id"]
            objects=objects.filter(account_id=account_id)
        if "event_id" in kwargs and kwargs["event_id"] is not None and kwargs["event_id"]>0 :
            event_id=kwargs["event_id"]
            objects=objects.filter(event_id=event_id)
        return objects.all().order_by('date_time')

    def accounting_document_line(self,*args, **kwargs):
        if "accounting_document_line_id" in kwargs and kwargs["accounting_document_line_id"] is not None:
            return self.objects.filter(pk=kwargs['accounting_document_line_id']).first() 
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
    def add_accounting_document_line(self,*args, **kwargs):
        accounting_document_line,message,result=(None,"",FAILED)
    
        bestankar=kwargs['bestankar']
        bedehkar=kwargs['bedehkar']
        if bedehkar==0 and bestankar==0:
            message="مبلغ بدهکار و بستانکار صفر وارد شده است."
            return result,message,accounting_document_line

            
        if bedehkar>0 and bestankar>0:
            message="مبلغ بدهکار و بستانکار ، هر دو وارد شده است."
            return result,message,accounting_document_line

        if bedehkar<0 or bestankar<0:
            message="مبلغ بدهکار یا بستانکار منفی وارد شده است."
            return result,message,accounting_document_line

        if not Permission(request=self.request).is_permitted(APP_NAME,OperationEnum.ADD,"accountingdocumentline"):
        # if not self.request.user.has_perm(APP_NAME+".add_accountingdocumentline"):
            message="دسترسی غیر مجاز"
            return result,message,accounting_document_line
        
        accounting_document_line=AccountingDocumentLine()

        if 'title' in kwargs:
            accounting_document_line.title=kwargs['title']
        if 'event_id' in kwargs:
            accounting_document_line.event_id=kwargs['event_id']
        if 'accounting_document_id' in kwargs:
            accounting_document_line.accounting_document_id=kwargs['accounting_document_id']
        if 'description' in kwargs:
            accounting_document_line.description=kwargs['description']
        if 'persian_date_time' in kwargs :
            kwargs['date_time']=PersianCalendar().to_gregorian(kwargs['persian_date_time'])
            # date_time=date_time,persian_date_time=kwargs['persian_date_time'])
            # accounting_document_line.date_time=date_time
        if 'bestankar' in kwargs  :
            accounting_document_line.bestankar=kwargs['bestankar']
        if 'bedehkar' in kwargs :
            accounting_document_line.bedehkar=kwargs['bedehkar'] 
        if 'date_time' in kwargs :
            # year=kwargs['date_time'][:2]
            # if year=="13" or year=="14":
            #     kwargs['date_time']=PersianCalendar().to_gregorian(kwargs["date_time"])
            accounting_document_line.date_time=kwargs['date_time'] 

        if 'account_code' in kwargs and kwargs['account_code'] is not None:
            account=AccountRepo(request=self.request).account(code=kwargs['account_code']) 
            if account is not None:
                accounting_document_line.account=account
        if 'account_id' in kwargs and kwargs['account_id'] is not None:
            accounting_document_line.account_id=kwargs['account_id'] 
        
        
        # if 'financial_year_id' in kwargs:
        #     payment.financial_year_id=kwargs['financial_year_id']
        # else:
        #     payment.financial_year_id=FinancialYear.get_by_date(date=payment.transaction_datetime).id

        if accounting_document_line.account.nature==AccountNatureEnum.ONLY_BESTANKAR and accounting_document_line.bedehkar>0:
            message=accounting_document_line.account.name+" ماهیت فقط بستانکار دارد"
            accounting_document_line=None
            return result,message,accounting_document_line
        if accounting_document_line.account.nature==AccountNatureEnum.ONLY_BEDEHKAR and accounting_document_line.bestankar>0:
            message=accounting_document_line.account.name+" ماهیت فقط بدهکار دارد"
            accounting_document_line=None
            return result,message,accounting_document_line


        accounting_document_line.save()
        accounting_document_line.account.normalize_total()
        result=SUCCEED
        message="با موفقیت اضافه گردید."
         

        me_profile=ProfileRepo(request=self.request).me
        new_log={}
        new_log['title']="خط سند مالی جدید "
        new_log['app_name']=APP_NAME
        new_log['url']=accounting_document_line.get_absolute_url()
        new_log['profile']=me_profile
        new_log['description']="خط سند مالی جدید با موفقیت اضافه گردید."
        LogRepo(request=self.request).add_log(**new_log)
        return result,message,accounting_document_line

    def delete_all(self,*args,**kwargs):
        
        if not self.request.user.has_perm(APP_NAME+".delete_accountingdocumentline"):
            message="دسترسی غیر مجاز"
            return result,message
        AccountingDocumentLine.objects.all().delete() 
                   
        result=SUCCEED
        message="همه حذف شدند."
        return result,message
    
    
    
    def add_event_accounting_document_line(self,*args, **kwargs):
        result,message,accounting_document_line=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_accountingdocumentline"):
            message="دسترسی غیر مجاز"
            return result,message,accounting_document_line

        event_id=kwargs['event_id']
        bestankar=kwargs['bestankar']
        bedehkar=kwargs['bedehkar']
        account_code=kwargs['account_code']
        accounting_document_id=kwargs['accounting_document_id']
        accounting_document_title=kwargs['accounting_document_title']

        account_repo=AccountRepo(request=self.request)
        event_repo=FinancialEventRepo(request=self.request)
        accounting_document_repo=AccountingDocumentRepo(request=self.request)

        event=event_repo.event(pk=event_id)
        account=account_repo.account(code=account_code)

        if accounting_document_id==0:
            result,message,accounting_document=accounting_document_repo.add_accounting_document(title=accounting_document_title)
        else:
            accounting_document=accounting_document_repo.accounting_document(pk=accounting_document_id)
        if account is not None and accounting_document is not None and event is not None:
            accounting_document_line=AccountingDocumentLine()
            accounting_document_line.event=event
            accounting_document_line.bestankar=bestankar
            accounting_document_line.bedehkar=bedehkar
            accounting_document_line.account=account
            accounting_document_line.date_time=event.event_datetime
            accounting_document_line.title=event.title
            accounting_document_line.accounting_document=accounting_document
            accounting_document_line.save()
            result=SUCCEED
            message="اضافه شد."
            return result,message,accounting_document_line
  


class InvoiceRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Invoice.objects.filter(id=0)
        profile=ProfileRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_invoice"):
                self.objects=Invoice.objects
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            codeee=str(filter_number(search_for))
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for) | Q(code=codeee) )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
       
    def roots(self,*args, **kwargs):
        objects=self.objects.filter(parent_id=None)
        return objects.all()

    def invoice(self,*args, **kwargs):
        if "invoice_id" in kwargs and kwargs["invoice_id"] is not None:
            return self.objects.filter(pk=kwargs['invoice_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
         
       

    def add_invoice(self,*args,**kwargs):
        result,message,invoice=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_invoice"):
            message="دسترسی غیر مجاز"
            return result,message,invoice

        invoice=Account()
        if 'name' in kwargs:
            invoice.name=kwargs["name"]
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                invoice.parent_id=kwargs["parent_id"]
        if 'color' in kwargs:
            invoice.color=kwargs["color"]
        if 'code' in kwargs:
            invoice.code=kwargs["code"]
        if 'priority' in kwargs:
            invoice.priority=kwargs["priority"]
        if 'type' in kwargs:
            invoice.type=kwargs["type"]

           
        (result,message,invoice)=invoice.save()
        return result,message,invoice



class FinancialEventRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=FinancialEvent.objects.filter(id=0)
        profile=ProfileRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_invoice"):
                self.objects=FinancialEvent.objects
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            codeee=str(filter_number(search_for))
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for) | Q(code=codeee) )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
       
    def roots(self,*args, **kwargs):
        objects=self.objects.filter(parent_id=None)
        return objects.all()

    def event(self,*args, **kwargs):
        if "event_id" in kwargs and kwargs["event_id"] is not None:
            return self.objects.filter(pk=kwargs['event_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
         
       

    def add_event(self,*args,**kwargs):
        result,message,event=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_event"):
            message="دسترسی غیر مجاز"
            return result,message,event

        event=Account()
        if 'name' in kwargs:
            event.name=kwargs["name"]
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                event.parent_id=kwargs["parent_id"]
        if 'color' in kwargs:
            event.color=kwargs["color"]
        if 'code' in kwargs:
            event.code=kwargs["code"]
        if 'priority' in kwargs:
            event.priority=kwargs["priority"]
        if 'type' in kwargs:
            event.type=kwargs["type"]

           
        (result,message,event)=event.save()
        return result,message,event

    def delete_all(self,*args, **kwargs):
        result=FAILED
        message=""
        if not self.request.user.has_perm(APP_NAME+".delete_event"):
            message="دسترسی غیر مجاز"
            return result,message
        FinancialEvent.objects.all().delete()
        return result,message
 
class PersonRepo():
    def __init__(self,request,*args, **kwargs):
        self.request=request
        self.me=None
        # profile=ProfileRepo(request=request).me
        self.objects=Person.objects

        
        self.objects=None
        if request.user.has_perm(APP_NAME+".view_person"):
            self.objects=Person.objects
        elif request.user.is_authenticated:
            self.objects=Person.objects.filter(profile__user_id=request.user.id)
                 
        else:
            self.objects=Person.objects.filter(pk=0)

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
            objects=objects.filter(Q(full_name__contains=search_for) | Q(melli_code__contains=search_for) | Q(code=search_for))
        return objects.all()
     
    def person(self,*args, **kwargs):
        if "person_id" in kwargs and kwargs["person_id"] is not None:
            return self.objects.filter(pk=kwargs['person_id']).first()
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
       
    def delete_all(self,*args,**kwargs):
        
        if not self.request.user.has_perm(APP_NAME+".delete_person"):
            message="دسترسی غیر مجاز"
            return result,message,person
        PersonCategory.objects.all().delete()
        Person.objects.all().delete()
        result=SUCCEED
        message="همه حذف شدند."
        return result,message
    
    def add_person(self,*args,**kwargs):
        result,message,person=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_person"):
            message="دسترسی غیر مجاز"
            return result,message,person

        person=Person()
        person_category_id=0
        categories=[]
        person_account_categories=[]


        if Person.objects.filter(code=kwargs['code']).first() is not None:
            message="کد وارد شده تکراری است."
            person=None
            return result,message,person
        if Person.objects.filter(melli_code=kwargs['melli_code']).first() is not None:
            message="کد ملی وارد شده تکراری است."
            person=None
            return result,message,person

  
        if 'type2' in kwargs:
            person.type2=kwargs["type2"]
        if 'type' in kwargs:
            person.type=kwargs["type"]
        if 'melli_code' in kwargs:
            person.melli_code=kwargs["melli_code"]
            
        if 'color' in kwargs:
            person.color=kwargs["color"]
        if 'first_name' in kwargs:
            person.first_name=kwargs["first_name"]
        if 'last_name' in kwargs:
            person.last_name=kwargs["last_name"]
        if 'bio' in kwargs:
            person.bio=kwargs["bio"]
        if 'email' in kwargs:
            person.email=kwargs["email"]
        if 'mobile' in kwargs:
            person.mobile=kwargs["mobile"]
        if 'prefix' in kwargs:
            person.prefix=kwargs["prefix"]
        if 'gender' in kwargs:
            person.gender=kwargs["gender"]
        if 'address' in kwargs:
            person.address=kwargs["address"]  
        if 'type' in kwargs:
            person.type=kwargs["type"] 
        if 'person_category_id' in kwargs and kwargs["person_category_id"] is not None:
            person_category_id=kwargs["person_category_id"]
            person_category=PersonCategory.objects.filter(pk=person_category_id).first()
            if person_category is not None:
                categories=[person_category.code]
         
            
        if 'person_account_categories' in kwargs:
            person_account_categories=kwargs["person_account_categories"]
             
 
        (result,message,person)=person.save()
        if result==FAILED:
            return result,message,person
        


        for person_account_category in person_account_categories: 
            person_category=PersonCategory.objects.filter(pk=person_account_category).first()
            person_account=PersonAccount(person=person,person_category=person_category)
            person_account.person=person
            person_account.person_category=person_category 
            person_account.save()
            pass
 
        return result,message,person

    def add_account_to_person(self,*args,**kwargs):
        result,message,account,person,action=FAILED,"",None,None,None
        if not self.request.user.has_perm(APP_NAME+".add_personaccount"):
            message="دسترسی غیر مجاز"
            return result,message,account,person,action
            
        person_account=PersonAccount()
        
        person_account.person_id=kwargs['person_id']
        person_account.person_category_id=kwargs['person_category_id']

        result,message,person_account=person_account.save()
        if result==FAILED:
            person_account=None
            return result,message,person_account,None,"ALREADY_EXISTED"

        action="ADDED"
        result=SUCCEED
        message=f"حساب مالی  {person_account.name} با موفقیت به شخص {person_account.person.full_name} اضافه شد."
            
        return result,message,person_account,person_account.person,action

    def remove_account_from_person(self,*args,**kwargs):
        result,message,person_account_id=FAILED,"",0
        if not self.request.user.has_perm(APP_NAME+".add_personaccount"):
            message="دسترسی غیر مجاز"
            return result,message,person_account_id
             
        person_id=kwargs['person_id']
        person_category_id=kwargs['person_category_id']

        person_account=PersonAccount.objects.filter(person_id=person_id).filter(person_category_id=person_category_id).first()
        if person_account is None:
            result=FAILED
            message="حساب مالی وجود ندارد."
            return result,message,person_account_id

        person_account_id=person_account.id
        try:
            person_account.delete()
            person_account_=PersonAccount.objects.filter(id=person_account_id).first()
            if person_account_ is None:
                result=SUCCEED
                message=f"حساب مالی  {person_account.name} با موفقیت از شخص {person_account.person.full_name} حذف شد."
        except:
            message="حذف نشد. "+"ابتدا رویداد های مالی مرتبط را حذف کنید."+"تا تراز فرد صفر شده و هیچ سندی با شخص در ارتباط نباشد."
            return result,message,person_account_id

        return result,message,person_account_id

 