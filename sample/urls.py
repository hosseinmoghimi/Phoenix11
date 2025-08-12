from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME

urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  

    path('samples/',login_required(views.SamplesView.as_view()),name="samples"),  
    path('add-sample/',login_required(apis.AddSampleApi.as_view()),name="add_sample"),
    path('sample/<int:pk>/',login_required(views.SampleView.as_view()),name="sample"), 


     
]
