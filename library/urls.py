from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME

urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  

    path('books/',login_required(views.BooksView.as_view()),name="books"),  
    path('add-book/',login_required(apis.AddBookApi.as_view()),name="add_book"),
    path('book/<int:pk>/',login_required(views.BookView.as_view()),name="book"), 


     
]
