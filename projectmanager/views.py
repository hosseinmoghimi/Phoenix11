from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from django.views import View
from .forms import *
from utility.enums import *
from .serializers import ProjectSerializer,RemoteClientSerializer,ProjectSerializerForGuantt
from .repo import ProjectRepo,RemoteClientRepo
from organization.views import OrganizationUnitRepo,OrganizationUnitSerializer
from .apps import APP_NAME
from core.views import CoreContext,PageContext,MessageView
from utility.calendar import PersianCalendar
from utility.currency import to_price
import json
from utility.enums import UnitNameEnum
from utility.views import NoPersmissionView
from utility.log import leolog
from accounting.views import ProductContext,PageContext,AddInvoiceContext,InvoiceSerializer,InvoiceLineWithInvoiceSerializer
from .enums import *
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
    project_s=json.dumps(ProjectSerializer(project).data)


    projects=project.childs.all()
    context['projects']=projects
    projects_s=json.dumps(ProjectSerializer(projects,many=True).data)
    context['projects_s']=projects_s
    if request.user.has_perm(APP_NAME+'.add_project'):
        context['add_sub_project_form']=AddSubProjectForm()
    context['project_s']=project_s
    context['WIDE_LAYOUT']=True

    if request.user.has_perm(APP_NAME+'.change_project'):
        context['edit_project_form']=EditProjectForm()
        context['colors_for_change_project']=(i[0] for i in ColorEnum.choices)
        all_organization_units=OrganizationUnitRepo(request=request).list()
        context['all_organization_units']=all_organization_units
        
        context['project_status_enum'] = (i[0] for i in ProjectStatusEnum.choices)
    return context


class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps

        return render(request,TEMPLATE_ROOT+"index.html",context)
# Create your views here. 



class ProjectGuanttView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        if context is None:
            return NoPersmissionView(request=request)
        project = ProjectRepo(request=request).project(*args, **kwargs)
        context['project'] = project
        projects=ProjectRepo(request=request).list(parent_id=project.pk).order_by('priority')
        context['projects'] = projects
        context['projects_s'] = json.dumps(ProjectSerializerForGuantt(projects, many=True).data)
        return render(request, TEMPLATE_ROOT+"guantt.html", context)


class ProjectView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        project=ProjectRepo(request=request).project(*args, **kwargs)
        project.normalize()
        if project is None:
            title='پروژه وجود ندارد'
            body='پروژه وجود ندارد'
            mv=MessageView(title=title,body=body)
            return mv.get(request=request)
        
        context.update(ProjectContext(request=request,project=project))



        
        invoices=project.invoices.all()
        invoices_s=json.dumps(InvoiceSerializer(invoices,many=True).data)
        context['invoices']=invoices
        context['invoices_s']=invoices_s

        
        invoice_lines=project.all_invocie_lines()
        invoice_lines_s=json.dumps(InvoiceLineWithInvoiceSerializer(invoice_lines,many=True).data)
        context['invoice_lines']=invoice_lines
        context['invoice_lines_s']=invoice_lines_s


        context['WIDE_LAYOUT']=True
        if request.user.has_perm(APP_NAME+".add_invoice"):
            context.update(AddInvoiceContext(request=request))


            

        context['WIDE_LAYOUT']=True
        if request.user.has_perm(APP_NAME+".change_project"):
            context['add_invoice_to_project_form']=AddInvoiceToProjectForm()


            

 
        
        remote_clients = project.remote_clients.all()
        context['remote_clients'] = remote_clients
        remote_clients_s = json.dumps(RemoteClientSerializer(remote_clients, many=True).data)
        context['remote_clients_s'] = remote_clients_s
        if request.user.has_perm(APP_NAME+".add_remoteclient"):
            context['operating_systems']=(i[0] for i in OperatingSystemNameEnum.choices)
            from accounting.repo import BrandRepo
            context['brands']=BrandRepo(request=request).list()
            context['add_remote_client_form'] = AddRemoteClientForm()
        return render(request,TEMPLATE_ROOT+"project.html",context)
# Create your views here. 


class ProjectTreeChartView(View):
    
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        project=ProjectRepo(request=request).project(*args, **kwargs)
        if project is None:
            title='پروژه وجود ندارد'
            body='پروژه وجود ندارد'
            mv=MessageView(title=title,body=body)
            return mv.get(request=request)
        
        context['project']=project  


        projects=project.all_sub_projects()
        context['projects']=projects
        projects_s=json.dumps(ProjectSerializer(projects,many=True).data)
        context['projects_s']=projects_s

        
        context['WIDE_LAYOUT']=True 
         
        
        pages=[{
                'title': f"""{project.title}""",
                'parent_id': project.parent_id,
                'parent': 0,
                'get_absolute_url': project.get_absolute_url(),
                'id': project.id,
                'pre_title': "",
                'color': project.color,
                'sub_title':to_price(project.total_price),
                }]
          
        for project in projects:
            pages.append({
                'title': f"""{project.title}""",
                'parent_id': project.parent_id,
                'parent': 0,
                'get_absolute_url': project.get_absolute_url(),
                'id': project.id,
                'pre_title': "",
                'color': project.color,
                'sub_title':to_price(project.amount),
                })

        context['pages_s'] = json.dumps(pages)
        return render(request,TEMPLATE_ROOT+"tree-chart.html",context) 

 
# Create your views here. 


class ProjectsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        projects = ProjectRepo(request=request).list(parent_id=None,*args, **kwargs)

        context['projects']=projects
        projects_s=json.dumps(ProjectSerializer(projects,many=True).data)
        context['projects_s']=projects_s
        if request.user.has_perm(APP_NAME+".add_project"):
            context['add_project_form']=AddProjectForm
            organizations=OrganizationUnitRepo(request=request).list()
            organizations_s=json.dumps(OrganizationUnitSerializer(organizations,many=True).data)
            context['organizations_s']=organizations_s
        return render(request,TEMPLATE_ROOT+"projects.html",context)
# Create your views here. 



class RemoteClientsView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        context['WIDE_LAYOUT'] = True
        if context is None:
            return notPersmissionView(request=request)
        remote_clients = RemoteClientRepo(request=request).list()
        context['remote_clients'] = remote_clients
        remote_clients_s = json.dumps(RemoteClientSerializer(remote_clients, many=True).data)
        context['remote_clients_s'] = remote_clients_s
        context['expand_remote_clients']=True
        # if request.user.has_perm(APP_NAME+".add_material"):
            # context['add_material_form']=AddMaterialForm()
        return render(request, TEMPLATE_ROOT+"remote-clients.html", context)


class RemoteClientView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        
        remote_client = RemoteClientRepo(request=request).remote_client(*args, **kwargs)
        context['remote_client'] = remote_client
        return render(request, TEMPLATE_ROOT+"remote-client.html", context)

