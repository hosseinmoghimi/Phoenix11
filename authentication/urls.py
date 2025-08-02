from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),
    path('settings/',login_required(views.IndexView.as_view()),name="settings"),
    path('login/',(views.LoginView.as_view()),name="login"),
    path('change-password/',login_required(views.ChangePasswordView.as_view()),name="change_password"),
    path('register/',login_required(views.IndexView.as_view()),name="register"),
    path('logout/',(views.LogoutView.as_view()),name="logout"),
    
    path('login_as/<int:pk>/',views.LoginAsViews.as_view(),name="login_as"),


    path('change-person-image/',login_required(views.ChangePersonImageView.as_view()),name="change_person_image"),
    path('persons/',login_required(views.PersonsView.as_view()),name="persons"),
    path('person/<int:pk>/',login_required(views.PersonView.as_view()),name="person"),
    path('select-person/',login_required(apis.SelectPersonApi.as_view()),name="select_person"),
    path('select-user/',login_required(apis.SelectUserApi.as_view()),name="select_user"),
    path('add-person/',login_required(apis.AddPersonApi.as_view()),name='add_person'),
    



]
