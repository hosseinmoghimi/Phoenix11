from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL,CURRENCY,VUE_VERSION_3,VUE_VERSION_2
from authentication.repo import ProfileRepo
from utility.repo import ParameterRepo,PictureRepo
from django.views import View
from .forms import *
from .serializer import CommentSerializer
from .apps import APP_NAME
from phoenix.server_apps import phoenix_apps
from utility.calendar import PersianCalendar
from utility.log import leolog
from django.utils import timezone
from core.views import CoreContext
from .repo import LikeRepo,CommentRepo
import json
LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='core/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"

def PageLikesContext(request,page,profile,*args, **kwargs):
    context={}
    like_repo = LikeRepo(request=request) 
    my_like = like_repo.my_like(page=page)
    likes_count = like_repo.likes_count(page=page)
    context['my_like']=my_like
    context['likes_count']=likes_count  
    if profile is not None:
        context['toggle_page_like_form']=TogglePageLikeForm()
    return context
 
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context
 
def PageCommentsContext(request,page,profile,*args, **kwargs):
    context={}
    comment_repo = CommentRepo(request=request) 
    page_comments=comment_repo.list(page_id=page.id)
    page_comments_s=json.dumps(CommentSerializer(page_comments,many=True).data)
    context['page_comments']=page_comments  
    context['page_comments_s']=page_comments_s  
    if profile is not None:
        context['add_page_comment_form']=AddPageCommentForm()
        context['delete_page_comment_form']=DeletePageCommentForm()
    return context
 