from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),
    path('settings/',login_required(views.IndexView.as_view()),name="settings"),
    path('toggle-like/',apis.TogglePageLikeApi.as_view(),name="toggle_like"),
    path('page/<int:pk>/',views.PageView.as_view(),name="page"),

]
