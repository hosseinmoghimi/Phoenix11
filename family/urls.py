from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME

urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  

    path('families/',login_required(views.FamiliesView.as_view()),name="families"),  
    path('add-family/',login_required(apis.AddFamilyApi.as_view()),name="add_family"),
    path('family/<int:pk>/',login_required(views.FamilyView.as_view()),name="family"), 


     
]
