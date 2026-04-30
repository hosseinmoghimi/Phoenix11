from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  
   
    path('add-table',login_required(apis.AddTableApi.as_view()),name="add_table"),
    path('table/<int:pk>/',login_required(views.TableView.as_view()),name="table"),  
    path('tables/',login_required(views.TablesView.as_view()),name="tables"),  
]
