from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME

urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  

    path('sample_classes/',login_required(views.SampleClassesView.as_view()),name="sample_classes"),  
    path('add-sample_class/',login_required(apis.AddSampleClassApi.as_view()),name="add_sample_class"),
    path('sample_class/<int:pk>/',login_required(views.SampleClassView.as_view()),name="sample_class"), 


     
]
