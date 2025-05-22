from .models import Account
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
        Event.objects.all().delete()
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

