from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),
    path('selection/',login_required(views.SelectionView.as_view()),name="selection"),
    path('settings/',login_required(views.IndexView.as_view()),name="settings"),
    path('accounts/',login_required(views.AccountsView.as_view()),name="accounts"),
    path('account/<int:pk>/',login_required(views.AccountView.as_view()),name="account"),
    path("tree-chart/<int:pk>/",login_required(views.TreeChartView.as_view()),name="tree_chart"),
]
