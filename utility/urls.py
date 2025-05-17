from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  
    path('parameters/',login_required(views.ParametersView.as_view()),name="parameters"), 
    path("get_parameters/",login_required(apis.GetParametersApi.as_view()),name="get_parameters"),
    path("set_parameter/",login_required(apis.SetParameterApi.as_view()),name="set_parameter"),

]
