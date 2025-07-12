from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    path('',login_required(views.IndexView.as_view()),name="index"),
    path('settings/',login_required(views.IndexView.as_view()),name="settings"),
    path('vehicles/',login_required(views.VehiclesView.as_view()),name="vehicles"),
    path('vehicle/<int:pk>/',login_required(views.VehicleView.as_view()),name="vehicle"),
    path('add-vehicle/ ',login_required(apis.AddVehicleApi.as_view()),name="add_vehicle"),


]
