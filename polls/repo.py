from .models import Poll
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


class PollRepo():

    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Poll.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=Poll.objects
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
        
    def poll(self,*args, **kwargs):
        if "poll_id" in kwargs and kwargs["poll_id"] is not None:
            return self.objects.filter(pk=kwargs['poll_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_poll(self,*args,**kwargs):
        result,message,poll=FAILED,"",None
        if len(Poll.objects.filter(title=kwargs["title"]))>0:
            message='عنوان تکراری برای نظرسنجی'
            return FAILED,message,None
        
            return FAILED,message,None
        if not self.request.user.has_perm(APP_NAME+".add_poll"):
            message="دسترسی غیر مجاز"
            return result,message,poll

        poll=Poll() 
    
        if 'title' in kwargs:
            poll.title=kwargs["title"]
          
        (result,message,poll)=poll.save()
        return result,message,poll