from . import views,apis
from django.contrib.auth.decorators import login_required
from django.urls import path
from .apps import APP_NAME

app_name=APP_NAME
urlpatterns = [
    path("",login_required(views.IndexView.as_view()),name="index"),
    path("profile/",login_required(views.ProfileView.as_view()),name="profile"),
]
