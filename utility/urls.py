from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  
    path('settings/',login_required(views.SettingsView.as_view()),name="settings"),  
    path('parameters/',login_required(views.ParametersView.as_view()),name="parameters"), 
    path("get_parameters/",login_required(apis.GetParametersApi.as_view()),name="get_parameters"),
    path("set_parameter/",login_required(apis.SetParameterApi.as_view()),name="set_parameter"),
    path("download_db/",login_required(views.BackupDBView.as_view()),name="download_db"),
    path("download_media/",login_required(views.DownloadMediaView.as_view()),name="download_media"),
    path("download_privates/",login_required(views.DownloadPrivatesView.as_view()),name="download_privates"),

]

