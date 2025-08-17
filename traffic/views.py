from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from .repo import TrafficRepo
from .serializers import TrafficSerializer
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
TEMPLATE_ROOT='traffic/'
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

 
 
class TrafficsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        traffics=TrafficRepo(request=request).list(*args, **kwargs)
        context["traffics"]=traffics
        traffics_s=json.dumps(TrafficSerializer(traffics,many=True).data)
        context["traffics_s"]=traffics_s
        if request.user.has_perm(APP_NAME+'.add_traffic'):
            context['add_traffic_form']=AddTrafficForm()
        return render(request,TEMPLATE_ROOT+"traffics.html",context)
# Create your views here. 
   
 
class TrafficView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        traffic=TrafficRepo(request=request).traffic(*args, **kwargs)
        context["traffic"]=traffic
        traffic_s=json.dumps(TrafficSerializer(traffic,many=False).data)
        context["traffic_s"]=traffic_s

        return render(request,TEMPLATE_ROOT+"traffic.html",context)
# Create your views here. 



  