from .models import Organization 
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
from .enums import *
 


class OrganizationRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Organization.objects.filter(id=0)
        profile=ProfileRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=Organization.objects
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
        
    def organization(self,*args, **kwargs):
        if "organization_id" in kwargs and kwargs["organization_id"] is not None:
            return self.objects.filter(pk=kwargs['organization_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_organization(self,*args,**kwargs):
        result,message,organization=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_organization"):
            message="دسترسی غیر مجاز"
            return result,message,organization
        leolog(kwargs=kwargs)
        organization=Organization()
        if 'name' in kwargs:
            organization.name=kwargs["name"]
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                organization.parent_id=kwargs["parent_id"]
        if 'bedehkar_id' in kwargs:
            organization.bedehkar_id=kwargs["bedehkar_id"]
        if 'bestankar_id' in kwargs:
            organization.bestankar_id=kwargs["bestankar_id"]
        if 'code' in kwargs:
            organization.code=kwargs["code"]
        if 'event_datetime' in kwargs:
            organization.event_datetime=kwargs["event_datetime"]
            organization.event_datetime=kwargs["event_datetime"]
            year=kwargs['event_datetime'][:2]
            if year=="13" or year=="14":
                kwargs['event_datetime']=PersianCalendar().to_gregorian(kwargs["event_datetime"])
            organization.event_datetime=kwargs['event_datetime']


        if 'title' in kwargs:
            organization.title=kwargs["title"]
        
        (result,message,organization)=organization.save()
        return result,message,organization

 