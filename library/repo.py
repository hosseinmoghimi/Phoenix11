from .models import Book
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


class BookRepo():

    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Book.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=Book.objects
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
        
    def book(self,*args, **kwargs):
        if "book_id" in kwargs and kwargs["book_id"] is not None:
            return self.objects.filter(pk=kwargs['book_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_book(self,*args,**kwargs):
        result,message,book=FAILED,"",None
        if len(Book.objects.filter(title=kwargs["title"]))>0:
            message='نام تکراری برای کتاب جدید'
            return FAILED,message,None
        
        if not self.request.user.has_perm(APP_NAME+".add_book"):
            message="دسترسی غیر مجاز"
            return result,message,book

        book=Book()  
        if 'title' in kwargs:
            book.title=kwargs["title"]
          
        (result,message,book)=book.save()
        return result,message,book