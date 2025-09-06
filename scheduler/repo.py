from .models import Appointment,Task
from .apps import APP_NAME
from .enums import *
from log.repo import LogRepo 
from django.db.models import Q
from django.shortcuts import reverse
from authentication.repo import PersonRepo
from accounting.repo import InvoiceLineItemUnitRepo
from utility.num import filter_number
from utility.calendar import PersianCalendar
from utility.constants import FAILED,SUCCEED
from utility.log import leolog
from .enums import *


class TaskRepo():

    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Task.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=Task.objects
                self.my_accounts=self.objects
                
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def task(self,*args, **kwargs):
        if "task_id" in kwargs and kwargs["task_id"] is not None:
            return self.objects.filter(pk=kwargs['task_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_task(self,*args,**kwargs):
        result,message,task=FAILED,"",None
       
        if not self.request.user.has_perm(APP_NAME+".add_task"):
            message="دسترسی غیر مجاز"
            return result,message,task

        task=Task() 
        if 'person_account_id' in kwargs:
            task.person_account_id=kwargs["person_account_id"]
        if 'title' in kwargs:
            task.title=kwargs["title"]
          
        (result,message,task)=task.save()
        return result,message,task

class AppointmentRepo():

    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Appointment.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=Appointment.objects
                self.my_accounts=self.objects
                
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def appointment(self,*args, **kwargs):
        if "appointment_id" in kwargs and kwargs["appointment_id"] is not None:
            return self.objects.filter(pk=kwargs['appointment_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_appointment(self,*args,**kwargs):
        result,message,appointment=FAILED,"",None
        
        if not self.request.user.has_perm(APP_NAME+".add_appointment"):
            message="دسترسی غیر مجاز"
            return result,message,appointment

        appointment=Appointment() 
        if 'persons_to_meet_id' in kwargs:
            appointment.person_account_id=kwargs["person_account_id"]
        if 'title' in kwargs:
            appointment.title=kwargs["title"]
          
        (result,message,appointment)=appointment.save()
        return result,message,appointment