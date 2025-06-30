from django.shortcuts import render,redirect
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from .repo import ProfileRepo
from django.views import View
from .forms import *
from .apps import APP_NAME
from phoenix.server_apps import phoenix_apps
from utility.calendar import PersianCalendar
from core.views import CoreContext,ParameterRepo,PictureRepo

LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='authentication/'
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

class LoginView(View):
    def get(self,request,*args, **kwargs): 
        messages=[]
        if 'messages' in kwargs:
            messages=kwargs['messages']
        context=getContext(request=request)
        context['login_form_header_image']=PictureRepo(request=request,app_name=APP_NAME).picture(name="تصویر لاگین")
        context['messages']=messages
        if 'next' in request.GET:
            context['next']=request.GET['next']
        else:
            context['next']=SITE_URL

        ProfileRepo(request=request).logout(request)
        context['login_form']=LoginForm()
        context['build_absolute_uri']=request.build_absolute_uri()
        build_absolute_uri=request.build_absolute_uri()
        ONLY_HTTPS=ParameterRepo(request=request,app_name=APP_NAME).parameter(name="فقط HTTPS",default=False).boolean_value
        if ONLY_HTTPS and "http://" in build_absolute_uri :
            build_absolute_uri=build_absolute_uri.replace("http:","https:")
            return redirect(build_absolute_uri)
        return render(request,TEMPLATE_ROOT+"login.html",context)
    def post(self,request,*args, **kwargs):
        context=getContext(request=request) 
        return render(request,TEMPLATE_ROOT+"login.html",context)
# Create your views here.

class ChangePasswordView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
           
        return render(request,TEMPLATE_ROOT+"login.html",context)
# Create your views here.
