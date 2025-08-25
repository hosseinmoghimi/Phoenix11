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


    
    path('warehouse_sheets/',login_required(views.WareHouseSheetsView.as_view()),name="warehouse_sheets"),  
    path('add_warehouse_sheet/',login_required(apis.AddWareHouseSheetApi.as_view()),name="add_warehouse_sheet"), 
    path('warehouse_sheet/<int:pk>/',login_required(views.WareHouseSheetView.as_view()),name="warehousesheet"), 

 
     path('select_warehouse/',login_required(apis.SelectWareHouseApi.as_view()),name="select_warehouse"), 
 
]
