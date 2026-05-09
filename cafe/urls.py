from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  
   
    path('add-table',login_required(apis.AddTableApi.as_view()),name="add_table"),
    path('add-desk',login_required(apis.AddDeskApi.as_view()),name="add_desk"),
    path('table/<int:pk>/',login_required(views.TableView.as_view()),name="table"),  
    path('tables/',login_required(views.TablesView.as_view()),name="tables"),  
    
    path('menus/',login_required(views.MenusView.as_view()),name="menus"),
    path('menu/<int:pk>/',login_required(views.MenuView.as_view()),name="menu"),
    path('desk-customer/<int:pk>/',login_required(views.DeskCustomerView.as_view()),name="deskcustomer"),
    path('desks/',login_required(views.DesksView.as_view()),name="desks"),
    path('desk/<int:pk>/',login_required(views.DeskView.as_view()),name="desk"),
    path('desk/<int:desk_id>/menu/<int:menu_id>/',login_required(views.DeskMenuView.as_view()),name="desk-menu"),
    path('add-menu/',login_required(apis.AddMenuApi.as_view()),name="add_menu"),
    
]
