from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  

    path('organization/add/',login_required(apis.AddOrganizationApi.as_view()),name="add_organization"),  
    path('organizations/',login_required(views.OrganizationsView.as_view()),name="organizations"),  
    path('organization/<int:pk>/',login_required(views.OrganizationView.as_view()),name="organization"),  
   
]
