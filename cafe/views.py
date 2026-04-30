from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from .repo import TableRepo
from .serializers import TableSerializer
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
TEMPLATE_ROOT='cafe/'
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

 
 
class TablesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        tables=TableRepo(request=request).list(*args, **kwargs)
        context["tables"]=tables
        tables_s=json.dumps(TableSerializer(tables,many=True).data)
        context["tables_s"]=tables_s

        if request.user.has_perm(APP_NAME+".add_table"):
            context['add_table_form']=AddTableForm()
        return render(request,TEMPLATE_ROOT+"tables.html",context)
# Create your views here. 

 
class TableView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        table=TableRepo(request=request).table(*args, **kwargs)
        table_s=json.dumps(TableSerializer(table,many=False).data)
        context["table_s"]=table_s
        context["table"]=table
        leolog(table=table,id=table.id,pk=table.pk)
        return render(request,TEMPLATE_ROOT+"table.html",context)
# Create your views here. 
 

   