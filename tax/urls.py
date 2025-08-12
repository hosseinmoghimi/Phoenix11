from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME

urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  

    path('taxes/',login_required(views.TaxesView.as_view()),name="taxes"),  
    path('add-tax/',login_required(apis.AddTaxApi.as_view()),name="add_tax"),
    path('tax/<int:pk>/',login_required(views.TaxView.as_view()),name="tax"), 


     
]
