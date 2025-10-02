from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from .repo import BookRepo
from .serializers import BookSerializer
from django.views import View
from .forms import *
from .apps import APP_NAME
from core.views import CoreContext,PageContext
from phoenix.server_apps import phoenix_apps
from utility.calendar import PersianCalendar
import json
from utility.enums import UnitNameEnum
from utility.log import leolog
from accounting.views import AddInvoiceLineContext,InvoiceContext,ProductContext
LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='library/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"
 
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context

def BookContext(request,book,*args, **kwargs):
    context=PageContext(request=request,page=book)
    return context
 
class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        phoenix_apps = sorted(phoenix_apps, key=lambda d: d['priority'])

        context['phoenix_apps']=phoenix_apps
        return render(request,TEMPLATE_ROOT+"index.html",context)
# Create your views here. 

 
 
class BooksView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        books=BookRepo(request=request).list(*args, **kwargs)
        context["books"]=books
        books_s=json.dumps(BookSerializer(books,many=True).data)
        context["books_s"]=books_s
        if request.user.has_perm(APP_NAME+'.add_book'):
            context['add_book_form']=AddBookForm()
        return render(request,TEMPLATE_ROOT+"books.html",context)
# Create your views here. 
   
 
class BookView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        book=BookRepo(request=request).book(*args, **kwargs)
        context.update(BookContext(request=request,book=book))
        context["book"]=book
        book_s=json.dumps(BookSerializer(book,many=False).data)
        context["book_s"]=book_s

        return render(request,TEMPLATE_ROOT+"book.html",context)
# Create your views here. 



  