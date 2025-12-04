from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME

urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  

    path('catalogs/',login_required(views.CatalogsView.as_view()),name="catalogs"),  
    path('add-catalog/',login_required(apis.AddCatalogApi.as_view()),name="add_catalog"),
    path('catalog/<int:pk>/',login_required(views.CatalogView.as_view()),name="catalog"), 


     
]
