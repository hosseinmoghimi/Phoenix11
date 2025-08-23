from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME

urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  

    path('polls/',login_required(views.PollesView.as_view()),name="polls"),  
    path('add-poll/',login_required(apis.AddPollApi.as_view()),name="add_poll"),
    path('poll/<int:pk>/',login_required(views.PollView.as_view()),name="poll"), 


     
]
