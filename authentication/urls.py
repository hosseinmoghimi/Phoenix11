from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),
    path('profiles/',login_required(views.IndexView.as_view()),name="profiles"),
    path('profile/<int:pk>/',login_required(views.IndexView.as_view()),name="profile"),
    path('select-profile/',login_required(apis.SelectProfileApi.as_view()),name="select_profile"),
    path('settings/',login_required(views.IndexView.as_view()),name="settings"),
    path('login/',login_required(views.LoginView.as_view()),name="login"),
    path('change-password/',login_required(views.ChangePasswordView.as_view()),name="change_password"),
    path('register/',login_required(views.IndexView.as_view()),name="register"),
    path('logout/',login_required(views.IndexView.as_view()),name="logout"),


    path('change-person-image/',login_required(views.ChangePersonImageView.as_view()),name="change_person_image"),
    path('persons/',login_required(views.PersonsView.as_view()),name="persons"),
    path('person/<int:pk>/',login_required(views.PersonView.as_view()),name="person"),
    path('select-person/',login_required(apis.SelectPersonApi.as_view()),name="select_person"),
    path('add-person/',login_required(apis.AddPersonApi.as_view()),name='add_person'),
    



]
