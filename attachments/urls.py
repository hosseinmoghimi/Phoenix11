from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    # path('',login_required(views.IndexView.as_view()),name="index"),
    path('toggle-like/',apis.TogglePageLikeApi.as_view(),name="toggle_like"),
    path('add-page-comment/',apis.AddPageCommentApi.as_view(),name="add_page_comment"),
    path('delete-page-comment/',apis.DeletePageCommentApi.as_view(),name="delete_page_comment"),

]
