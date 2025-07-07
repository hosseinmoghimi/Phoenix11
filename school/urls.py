from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  

    path('schools/',login_required(views.SchoolsView.as_view()),name="schools"),  
    path('add-school-item',login_required(apis.AddSchoolApi.as_view()),name="add_school_item"),
    path('school/<int:pk>/',login_required(views.SchoolView.as_view()),name="school"),  
    
]
