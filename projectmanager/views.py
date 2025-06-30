from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from django.views import View
from .forms import *
from .serializers import ProjectSerializer
from .repo import ProjectRepo
from .apps import APP_NAME
from core.views import CoreContext,PageContext
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


def ProjectContext(request,food_item,*args, **kwargs):
    context=PageContext(request=request,page=food_item)
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
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        phoenix_apps = sorted(phoenix_apps, key=lambda d: d['priority'])

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
        return render(request,TEMPLATE_ROOT+"projects.html",context)
# Create your views here. 

  