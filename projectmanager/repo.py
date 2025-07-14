from .models import Project,RemoteClient
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

 


    def edit_project(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".change_project"):
            return None
        project=self.project(*args, **kwargs)
        if project is not None:
            if 'percentage_completed' in kwargs:
                project.percentage_completed=kwargs['percentage_completed']
            if 'start_datetime' in kwargs:
                project.start_datetime=kwargs['start_datetime']
            if 'end_datetime' in kwargs:
                project.end_datetime=kwargs['end_datetime']
            if 'status' in kwargs:
                project.status=kwargs['status']
            if 'contractor_id' in kwargs:
                project.contractor_id=kwargs['contractor_id']
            if 'percentage_completed' in kwargs:
                project.percentage_completed=kwargs['percentage_completed']
            if 'weight' in kwargs:
                project.weight=kwargs['weight']
            if 'parent_id' in kwargs:
                parent_id=kwargs['parent_id']
                if parent_id<1:
                    project.parent=None
                elif parent_id>0 and len(Project.objects.filter(pk=parent_id))==1 and not parent_id==project.pk:
                    project.parent_id=parent_id
            if 'employer_id' in kwargs:
                project.employer_id=kwargs['employer_id']
            if 'title' in kwargs:
                project.title=kwargs['title']
            if 'weight' in kwargs:
                project.weight=kwargs['weight']
                pass
            if 'priority' in kwargs:
                project.priority=kwargs['priority']
                pass
            if 'archive' in kwargs:
                project.archive=kwargs['archive']
            project.save()
            return project


class RemoteClientRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=RemoteClient.objects.all().order_by("-id")
        self.profile=ProfileRepo(*args, **kwargs).me
       

    def remote_client(self, *args, **kwargs):
        pk=0
        if 'remote_client_id' in kwargs:
            pk=kwargs['remote_client_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
           
            objects = objects.filter(Q(name__contains=search_for)|Q(description__contains=search_for)|Q(local_ip__contains=search_for)|Q(remote_ip__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home'])) 
         

        return objects.all() 

    def add_remote_client(self,*args, **kwargs):
        result,message,remote_client=None,FAILED,""
        if not self.user.has_perm(APP_NAME+'.add_remoteclient'):
            message="شما مجوز لازم را برای افزودن سیستم کلاینت ندارید."
            return result,message,remote_client
        project_id=kwargs['project_id']
        a=kwargs.pop("project_id")
        remote_client=RemoteClient(*args, **kwargs)
        if remote_client.brand_id==0 or remote_client.brand_id is None:
            remote_client.brand=None
        remote_client.save()
        project=Project.objects.filter(pk=project_id).first()
        if project is not None:
            project.remote_clients.add(remote_client)
            result=SUCCEED
            message="با موفقیت اضافه شد."
        else:
            message="پروژه مرتبط یافت نشد."

        return result,message,remote_client

 