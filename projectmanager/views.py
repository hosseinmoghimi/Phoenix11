from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from django.views import View
from .forms import *
from .serializers import ProjectSerializer
from .repo import ProjectRepo
from organization.views import OrganizationRepo,OrganizationSerializer
from .apps import APP_NAME
from core.views import CoreContext,PageContext,MessageView
from utility.calendar import PersianCalendar
import json
from utility.enums import UnitNameEnum
from utility.log import leolog
from accounting.views import ProductContext,PageContext
LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='projectmanager/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"
 
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context

def ProjectContext(request,project,*args, **kwargs):
    context=PageContext(request=request,page=project)
    context['project']=project
    context['WIDE_LAYOUT']=True
    return context


class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps

        return render(request,TEMPLATE_ROOT+"index.html",context)
# Create your views here. 


class ProjectView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        project=ProjectRepo(request=request).project(*args, **kwargs)
        if project is None:
            mv=MessageView()
            return mv.get(request=request)
        
        context.update(ProjectContext(request=request,project=project))

        return render(request,TEMPLATE_ROOT+"project.html",context)
# Create your views here. 


class ProjectsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        projects = ProjectRepo(request=request).list(*args, **kwargs)

        context['projects']=projects
        projects_s=json.dumps(ProjectSerializer(projects,many=True).data)
        context['projects_s']=projects_s
        if request.user.has_perm(APP_NAME+".add_project"):
            context['add_project_form']=AddProjectForm
            organizations=OrganizationRepo(request=request).list()
            organizations_s=json.dumps(OrganizationSerializer(organizations,many=True).data)
            context['organizations_s']=organizations_s
        return render(request,TEMPLATE_ROOT+"projects.html",context)
# Create your views here. 
