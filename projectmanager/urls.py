from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  

    path('project/add/sub/',login_required(apis.AddSubProjectApi.as_view()),name="add_sub_project"),  
    path('project/add/',login_required(apis.AddProjectApi.as_view()),name="add_project"),  
    path('projects/',login_required(views.ProjectsView.as_view()),name="projects"),  
    path('project/<int:pk>/',login_required(views.ProjectView.as_view()),name="project"),  
    path('project/',login_required(views.ProjectView.as_view()),name="project_null"),  
    path('edit-project/',login_required(apis.EditProjectApi.as_view()),name="edit_project"),  

    path('add-project-invoice/',login_required(apis.AddProjectInvoiceApi.as_view()),name="add_project_invoice"),

    path('remote_client/add/',login_required(apis.AddRemoteClientApi.as_view()),name="add_remote_client"),  
    path('remoteclients/',login_required(views.RemoteClientsView.as_view()),name="remoteclients"),  
    path('remoteclient/<int:pk>/',login_required(views.RemoteClientView.as_view()),name="remoteclient"),  
   
]
