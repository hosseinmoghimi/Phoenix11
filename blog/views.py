from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from .repo import BlogRepo
from .serializers import BlogSerializer
from django.views import View
from .forms import *
from .apps import APP_NAME
from core.views import CoreContext
from phoenix.server_apps import phoenix_apps
from utility.calendar import PersianCalendar
import json
from utility.enums import UnitNameEnum
from utility.log import leolog
from accounting.views import AddInvoiceLineContext,InvoiceContext,ProductContext
LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='blog/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"
 
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
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

 
 
class BlogsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        blogs=BlogRepo(request=request).list(*args, **kwargs)
        context["blogs"]=blogs
        blogs_s=json.dumps(BlogSerializer(blogs,many=True).data)
        context["blogs_s"]=blogs_s
        if request.user.has_perm(APP_NAME+'.add_blog'):
            context['add_blog_form']=AddBlogForm()
        return render(request,TEMPLATE_ROOT+"blogs.html",context)
# Create your views here. 
   
 
class BlogView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        blog=BlogRepo(request=request).blog(*args, **kwargs)
        context["blog"]=blog
        blog_s=json.dumps(BlogSerializer(blog,many=False).data)
        context["blog_s"]=blog_s

        return render(request,TEMPLATE_ROOT+"blog.html",context)
# Create your views here. 



  