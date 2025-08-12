from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from .repo import SampleRepo
from .serializers import SampleSerializer
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
TEMPLATE_ROOT='sample/'
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

 
 
class SamplesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        samples=SampleRepo(request=request).list(*args, **kwargs)
        context["samples"]=samples
        samples_s=json.dumps(SampleSerializer(samples,many=True).data)
        context["samples_s"]=samples_s
        if request.user.has_perm(APP_NAME+'.add_sample'):
            context['add_sample_form']=AddSampleForm()
        return render(request,TEMPLATE_ROOT+"samples.html",context)
# Create your views here. 
   
 
class SampleView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        sample=SampleRepo(request=request).sample(*args, **kwargs)
        context["sample"]=sample
        sample_s=json.dumps(SampleSerializer(sample,many=False).data)
        context["sample_s"]=sample_s

        return render(request,TEMPLATE_ROOT+"sample.html",context)
# Create your views here. 



  