from .models import Family
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


class FamilyRepo():

    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Family.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=Family.objects
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
        
    def family(self,*args, **kwargs):
        if "family_id" in kwargs and kwargs["family_id"] is not None:
            return self.objects.filter(pk=kwargs['family_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_family(self,*args,**kwargs):
        result,message,family=FAILED,"",None
        if len(Family.objects.filter(name=kwargs["name"]))>0:
            message='نام تکراری برای آموزشگاه جدید'
            return FAILED,message,None
        if len(Family.objects.filter(person_account_id=kwargs["person_account_id"]))>0:
            message='حساب تکراری برای آموزشگاه جدید'
            return FAILED,message,None
        if not self.request.user.has_perm(APP_NAME+".add_family"):
            message="دسترسی غیر مجاز"
            return result,message,family

        family=Family() 
        if 'person_account_id' in kwargs:
            family.person_account_id=kwargs["person_account_id"]
        if 'name' in kwargs:
            family.name=kwargs["name"]
          
        (result,message,family)=family.save()
        return result,message,family