from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from .repo import SampleClassRepo
from .serializers import SampleClassSerializer
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
TEMPLATE_ROOT='sample_app/'
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

 
 
class SampleClassesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        sample_classes=SampleClassRepo(request=request).list(*args, **kwargs)
        context["sample_classes"]=sample_classes
        sample_classes_s=json.dumps(SampleClassSerializer(sample_classes,many=True).data)
        context["sample_classes_s"]=sample_classes_s
        if request.user.has_perm(APP_NAME+'.add_sample_class'):
            context['add_sample_class_form']=AddSampleClassForm()
        return render(request,TEMPLATE_ROOT+"sample_classes.html",context)
# Create your views here. 
   
 
class SampleClassView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        sample_class=SampleClassRepo(request=request).sample_class(*args, **kwargs)
        context["sample_class"]=sample_class
        sample_class_s=json.dumps(SampleClassSerializer(sample_class,many=False).data)
        context["sample_class_s"]=sample_class_s

        return render(request,TEMPLATE_ROOT+"sample_class.html",context)
# Create your views here. 



  