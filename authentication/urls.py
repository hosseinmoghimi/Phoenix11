from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),
    path('profile/<int:pk>/',login_required(views.IndexView.as_view()),name="profile"),
    path('settings/',login_required(views.IndexView.as_view()),name="settings"),
    path('login/',login_required(views.LoginView.as_view()),name="login"),
    path('change-password/',login_required(views.ChangePasswordView.as_view()),name="change_password"),
    path('register/',login_required(views.IndexView.as_view()),name="register"),
    path('logout/',login_required(views.IndexView.as_view()),name="logout"),
    



]
