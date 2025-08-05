from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from .repo import DrugRepo
from .serializers import DrugSerializer
from django.views import View
from .forms import *
from .apps import APP_NAME
from core.views import CoreContext,PageContext
from utility.calendar import PersianCalendar
import json
from utility.enums import UnitNameEnum
from utility.log import leolog
from accounting.views import AddProductContext,ProductContext
LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='health/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"
 
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context


def DrugContext(request,drug,*args, **kwargs):
    context=PageContext(request=request,page=drug)
    return context
 
 
class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        return render(request,TEMPLATE_ROOT+"index.html",context)
# Create your views here. 

 
 
class DrugsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        drugs=DrugRepo(request=request).list(*args, **kwargs)
        context["drugs"]=drugs
        drugs_s=json.dumps(DrugSerializer(drugs,many=True).data)
        context["drugs_s"]=drugs_s
        if request.user.has_perm(APP_NAME+'.add_drug'):
            context['add_drug_form']=AddDrugForm()
            context.update(AddProductContext(request=request))
        return render(request,TEMPLATE_ROOT+"drugs.html",context)
# Create your views here. 




 
class DrugView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        drug=DrugRepo(request=request).drug(*args, **kwargs)
        context["drug"]=drug
        context.update(ProductContext(request=request,product=drug))
        return render(request,TEMPLATE_ROOT+"drug.html",context)
# Create your views here. 


