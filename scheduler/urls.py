from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME

urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  

    path('appointments/',login_required(views.AppointmentsView.as_view()),name="appointments"),  
    path('add-appointment/',login_required(apis.AddAppointmentApi.as_view()),name="add_appointment"),
    path('appointment/<int:pk>/',login_required(views.AppointmentView.as_view()),name="appointment"), 


    path('tasks/',login_required(views.TasksView.as_view()),name="tasks"),  
    path('add-task/',login_required(apis.AddTaskApi.as_view()),name="add_task"),
    path('task/<int:pk>/',login_required(views.TaskView.as_view()),name="task"), 


     
]
