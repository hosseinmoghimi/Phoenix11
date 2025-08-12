from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from .repo import TaxRepo
from .serializers import TaxSerializer
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
TEMPLATE_ROOT='tax/'
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

 
 
class TaxesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        taxs=TaxRepo(request=request).list(*args, **kwargs)
        context["taxs"]=taxs
        taxs_s=json.dumps(TaxSerializer(taxs,many=True).data)
        context["taxs_s"]=taxs_s
        if request.user.has_perm(APP_NAME+'.add_tax'):
            context['add_tax_form']=AddTaxForm()
        return render(request,TEMPLATE_ROOT+"taxes.html",context)
# Create your views here. 
   
 
class TaxView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        tax=TaxRepo(request=request).tax(*args, **kwargs)
        context["tax"]=tax
        tax_s=json.dumps(TaxSerializer(tax,many=False).data)
        context["tax_s"]=tax_s

        return render(request,TEMPLATE_ROOT+"tax.html",context)
# Create your views here. 



  