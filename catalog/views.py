from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from .repo import CatalogRepo
from .serializers import CatalogSerializer
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
TEMPLATE_ROOT='catalog/'
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
        return render(request,TEMPLATE_ROOT+"index.html",context)

 
 
class CatalogsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        catalogs=CatalogRepo(request=request).list(*args, **kwargs)
        context["catalogs"]=catalogs
        catalogs_s=json.dumps(CatalogSerializer(catalogs,many=True).data)
        context["catalogs_s"]=catalogs_s
        if request.user.has_perm(APP_NAME+'.add_catalog'):
            context['add_catalog_form']=AddCatalogForm()
        return render(request,TEMPLATE_ROOT+"catalogs.html",context)
# Create your views here. 
   
 
class CatalogView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        catalog=CatalogRepo(request=request).catalog(*args, **kwargs)
        context["catalog"]=catalog
        catalog_s=json.dumps(CatalogSerializer(catalog,many=False).data)
        context["catalog_s"]=catalog_s

        return render(request,TEMPLATE_ROOT+"catalog.html",context)
# Create your views here. 


