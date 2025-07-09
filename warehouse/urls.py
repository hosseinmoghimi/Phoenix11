from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  

    path('warehouses/',login_required(views.WareHousesView.as_view()),name="warehouses"),  
    path('add-warehouse/',login_required(apis.AddWareHouseApi.as_view()),name="add_warehouse"),
    path('warehouse/<int:pk>/',login_required(views.WareHouseView.as_view()),name="warehouse"), 
 
    
]
