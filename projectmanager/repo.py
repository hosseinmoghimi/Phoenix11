from .models import Project 
from .apps import APP_NAME
from .enums import *
from log.repo import LogRepo 
from django.db.models import Q
from django.shortcuts import reverse
from authentication.repo import ProfileRepo
from accounting.repo import InvoiceLineItemUnitRepo
from utility.num import filter_number
from utility.calendar import PersianCalendar
from utility.constants import FAILED,SUCCEED
from utility.log import leolog
from .enums import *
 


class ProjectRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Project.objects.filter(id=0)
        profile=ProfileRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=Project.objects
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
        
    def project(self,*args, **kwargs):
        if "project_id" in kwargs and kwargs["project_id"] is not None:
            return self.objects.filter(pk=kwargs['project_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_project(self,*args,**kwargs):
        result,message,project=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_project"):
            message="دسترسی غیر مجاز"
            return result,message,project
        leolog(kwargs=kwargs)
        project=Project()
        if 'title' in kwargs:
            project.title=kwargs["title"]
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                project.parent_id=kwargs["parent_id"]
        if 'employer_id' in kwargs:
            project.employer_id=kwargs["employer_id"]
        if 'contractor_id' in kwargs:
            project.contractor_id=kwargs["contractor_id"]
        if 'type' in kwargs:
            project.type=kwargs["type"]
        if 'weight' in kwargs:
            project.weight=kwargs["weight"]
        if 'percentage_completed' in kwargs:
            project.percentage_completed=kwargs["percentage_completed"]
        if 'start_datetime' in kwargs:
            project.start_datetime=kwargs["start_datetime"]
            project.start_datetime=kwargs["start_datetime"]
            year=kwargs['start_datetime'][:2]
            if year=="13" or year=="14":
                kwargs['start_datetime']=PersianCalendar().to_gregorian(kwargs["start_datetime"])
            project.start_datetime=kwargs['start_datetime']

 
        if 'end_datetime' in kwargs:
            project.end_datetime=kwargs["end_datetime"]
            project.end_datetime=kwargs["end_datetime"]
            year=kwargs['end_datetime'][:2]
            if year=="13" or year=="14":
                kwargs['end_datetime']=PersianCalendar().to_gregorian(kwargs["end_datetime"])
            project.end_datetime=kwargs['end_datetime']

 
        if 'event_datetime' in kwargs:
            project.event_datetime=kwargs["event_datetime"]
            project.event_datetime=kwargs["event_datetime"]
            year=kwargs['event_datetime'][:2]
            if year=="13" or year=="14":
                kwargs['event_datetime']=PersianCalendar().to_gregorian(kwargs["event_datetime"])
            project.event_datetime=kwargs['event_datetime']

 
        
        (result,message,project)=project.save()
        return result,message,project

 