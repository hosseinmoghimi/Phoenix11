from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL,CURRENCY,VUE_VERSION_3,VUE_VERSION_2
from authentication.repo import ProfileRepo
from utility.repo import ParameterRepo,PictureRepo
from django.views import View
from .forms import *
from .serializer import CommentSerializer,LinkSerializer,DownloadSerializer
from .apps import APP_NAME
from phoenix.server_apps import phoenix_apps
from utility.calendar import PersianCalendar
from utility.log import leolog
from django.utils import timezone
from core.views import CoreContext
from .repo import LikeRepo,CommentRepo,LinkRepo,DownloadRepo
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
    comments=comment_repo.list(page_id=page.id)
    comments_s=json.dumps(CommentSerializer(comments,many=True).data)
    context['comments']=comments  
    context['comments_s']=comments_s  
    if profile is not None:
        context['add_comment_form']=AddPageCommentForm()
        context['delete_comment_form']=DeletePageCommentForm()
    return context
 
def PageLinksContext(request,page,profile,*args, **kwargs):
    context={}
    link_repo = LinkRepo(request=request) 
    links=link_repo.list(page_id=page.id)
    links_s=json.dumps(LinkSerializer(links,many=True).data)
    context['links']=links  
    context['links_s']=links_s  
    if profile is not None:
        context['add_link_form']=AddLinkForm()
    return context

def PageDownloadsContext(request,page,profile,*args, **kwargs):
    context={}
    download_repo = DownloadRepo(request=request) 
    downloads=download_repo.list(page_id=page.id)
    downloads_s=json.dumps(DownloadSerializer(downloads,many=True).data)
    context['downloads']=downloads  
    context['downloads_s']=downloads_s  
    if profile is not None:
        context['add_download_form']=AddDownloadForm()
    return context

class DownloadView(View):
    def get(self, request, *args, **kwargs): 
        me = ProfileRepo(request=request).me
        download = DownloadRepo(request=request).download(*args, **kwargs)
        if download is None or (me is None and not download.is_open):
            pass
        elif request.user.has_perm("attachments.change_download") or download.is_open or me in download.profiles.all():
            file_path = str(download.file.path)
            # return JsonResponse({'download:':str(file_path)})
            import os
            from django.http import HttpResponse
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(
                        fh.read(), content_type="application/force-download")
                    response['Content-Disposition'] = 'inline; filename=  '+ os.path.basename(file_path)
                    download.download_counter += 1
                    download.save()
                    return response
                    
        # if self.access(request=request,*args, **kwargs) and document is not None:
        #     return document.download_response()
        # from utility.views import MessageView
        from core.views import MessageView
        message_view = MessageView(request=request)
        message_view.links = []
        message_view.message_color = 'warning'
        message_view.has_home_link = True
        message_view.header_color = "rose"
        message_view.message_icon = ''
        message_view.header_icon = '<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>'
        message_view.body = ' شما مجوز دسترسی به این صفحه را ندارید.'
        message_view.title = 'دسترسی غیر مجاز'
        if download is None:
            message_view.body = 'دانلود مورد نظر شما پیدا نشد.'
            message_view.title = 'دانلود مورد نظر پیدا نشد.'
        else:
            from .models import Link
            message_view.links.append(Link(title='تلاش مجدد', color="warning",
                                  icon_material="apartment", url=download.get_download_url))

        return message_view.response()
        
      