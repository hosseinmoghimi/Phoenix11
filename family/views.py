from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from .repo import FamilyRepo
from .serializers import FamilySerializer
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
TEMPLATE_ROOT='family/'
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

 
 
class FamiliesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        families=FamilyRepo(request=request).list(*args, **kwargs)
        context["families"]=families
        families_s=json.dumps(FamilySerializer(families,many=True).data)
        context["families_s"]=families_s
        if request.user.has_perm(APP_NAME+'.add_family'):
            context['add_family_form']=AddFamilyForm()
        return render(request,TEMPLATE_ROOT+"families.html",context)
# Create your views here. 
   
 
class FamilyView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        family=FamilyRepo(request=request).family(*args, **kwargs)
        context["family"]=family
        family_s=json.dumps(FamilySerializer(family,many=False).data)
        context["family_s"]=family_s

        return render(request,TEMPLATE_ROOT+"family.html",context)
# Create your views here. 



  