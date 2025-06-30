from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  

    path('project/add/',login_required(apis.AddProjectApi.as_view()),name="add_project"),  
    path('projects/',login_required(views.ProjectsView.as_view()),name="projects"),  
    path('project/<int:pk>/',login_required(views.ProjectView.as_view()),name="project"),  
   
]
