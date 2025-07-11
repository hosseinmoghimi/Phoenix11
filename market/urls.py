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
    path('desk-customer/<int:pk>/',login_required(views.ProductView.as_view()),name="deskcustomer"),
    path('shop/<int:pk>/',login_required(views.ProductView.as_view()),name="shop"),

    path('category/<int:pk>/',login_required(views.CategoryView.as_view()),name="category"),
    path('categories/',login_required(views.CategoriesView.as_view()),name="categories"),
    
    path('menus/',login_required(views.MenusView.as_view()),name="menus"),
    path('menu/<int:pk>/',login_required(views.MenuView.as_view()),name="menu"),
    path('desks/',login_required(views.DesksView.as_view()),name="desks"),
    path('desk/<int:pk>/',login_required(views.DeskView.as_view()),name="desk"),
    path('desk/<int:desk_id>/menu/<int:menu_id>/',login_required(views.DeskMenuView.as_view()),name="desk-menu"),
    path('menu/add/ ',login_required(apis.AddMenuApi.as_view()),name="add_menu"),
    path('add-to-cart/ ',login_required(apis.AddMenuApi.as_view()),name="add_to_cart"),


]
