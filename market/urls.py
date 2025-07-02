from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    path('',login_required(views.IndexView.as_view()),name="index"),
    path('settings/',login_required(views.IndexView.as_view()),name="settings"),
    path('products/',login_required(views.ProductsView.as_view()),name="products"),
    path('product/<int:pk>/',login_required(views.ProductView.as_view()),name="product"),
    path('supplier/<int:pk>/',login_required(views.ProductView.as_view()),name="supplier"),
    path('shipper/<int:pk>/',login_required(views.ProductView.as_view()),name="shipper"),
    path('customer/<int:pk>/',login_required(views.ProductView.as_view()),name="customer"),
    path('shop/<int:pk>/',login_required(views.ProductView.as_view()),name="shop"),

    
    path('menus/',login_required(views.MenusView.as_view()),name="menus"),
    path('menu/<int:pk>/',login_required(views.MenuView.as_view()),name="menu"),
    path('menu/add/ ',login_required(apis.AddMenuApi.as_view()),name="add_menu"),


]
