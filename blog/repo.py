from .models import Blog
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


class BlogRepo():

    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Blog.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=Blog.objects
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
        
    def blog(self,*args, **kwargs):
        if "blog_id" in kwargs and kwargs["blog_id"] is not None:
            return self.objects.filter(pk=kwargs['blog_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_blog(self,*args,**kwargs):
        result,message,blog=FAILED,"",None
        if len(Blog.objects.filter(title=kwargs["title"]))>0:
            message='عنوان تکراری برای بلاگ جدید'
            return FAILED,message,None
        
            return FAILED,message,None
        if not self.request.user.has_perm(APP_NAME+".add_blog"):
            message="دسترسی غیر مجاز"
            return result,message,blog

        blog=Blog() 
        if 'title' in kwargs:
            blog.title=kwargs["title"]
        
        (result,message,blog)=blog.save()
        return result,message,blog