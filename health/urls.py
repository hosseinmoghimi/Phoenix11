from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  
 
    path('add-drug',login_required(apis.AddDrugApi.as_view()),name="add_drug"),
    path('drugs/',login_required(views.DrugsView.as_view()),name="drugs"),
    path('drug/<int:pk>/',login_required(views.DrugView.as_view()),name="drug"),  
    
]
