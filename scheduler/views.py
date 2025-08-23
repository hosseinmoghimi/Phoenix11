from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from .repo import AppointmentRepo
from .serializers import AppointmentSerializer
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
TEMPLATE_ROOT='scheduler/'
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

 
 
class AppointmentesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        appointments=AppointmentRepo(request=request).list(*args, **kwargs)
        context["appointments"]=appointments
        appointments_s=json.dumps(AppointmentSerializer(appointments,many=True).data)
        context["appointments_s"]=appointments_s
        if request.user.has_perm(APP_NAME+'.add_appointment'):
            context['add_appointment_form']=AddAppointmentForm()
        return render(request,TEMPLATE_ROOT+"appointments.html",context)
# Create your views here. 
   
 
class AppointmentView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        appointment=AppointmentRepo(request=request).appointment(*args, **kwargs)
        context["appointment"]=appointment
        appointment_s=json.dumps(AppointmentSerializer(appointment,many=False).data)
        context["appointment_s"]=appointment_s

        return render(request,TEMPLATE_ROOT+"appointment.html",context)
# Create your views here. 



  