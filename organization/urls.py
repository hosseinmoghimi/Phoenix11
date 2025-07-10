from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  

    path('organization_unit/add/',login_required(apis.AddOrganizationUnitApi.as_view()),name="add_organization_unit"),  
    path('organization_units/',login_required(views.OrganizationUnitsView.as_view()),name="organization_units"),  
    path('organization_unit/<int:pk>/',login_required(views.OrganizationUnitView.as_view()),name="organizationunit"),  
   
]
