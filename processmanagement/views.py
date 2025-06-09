from django.shortcuts import render
from django.views import View
from phoenix.server_apps import phoenix_apps
from core.views import CoreContext
from .apps import APP_NAME
LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='authentication/'

 

    
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)

    context['name2']="name 2222"
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context




class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="authentication 3333"
        return render(request,TEMPLATE_ROOT+"index.html",context) 


class ProfileView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['profile']="profile 534463"
        return render(request,TEMPLATE_ROOT+"profile.html",context) 