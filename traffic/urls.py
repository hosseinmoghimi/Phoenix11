from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME

urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  

    path('traffics/',login_required(views.TrafficsView.as_view()),name="traffics"),  
    path('add-traffic/',login_required(apis.AddTrafficApi.as_view()),name="add_traffic"),
    path('traffic/<int:pk>/',login_required(views.TrafficView.as_view()),name="traffic"), 


     
]
