# from core.serializers import PageBriefSerializer, PageCommentSerializer, PageDecodeSerializer, PageDownloadSerializer, PageImageSerializer, PageLikeSerializer, PageLinkSerializer, PagePermissionSerializer, PageSerializer, PageTagSerializer, ParameterSerializer, TagSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from .forms import *
# from .repo import ContactMessageRepo, PageCommentRepo, PageLinkRepo, PagePermissionRepo, PageRepo, PageTagRepo,  ParameterRepo,PageDownloadRepo,PageImageRepo
from .repo import LikeRepo,CommentRepo,LinkRepo,DownloadRepo,ImageRepo
from .serializer import  CommentSerializer,LinkSerializer,DownloadSerializer,ImageSerializer
from utility.constants import SUCCEED, FAILED
from utility.utils import str_to_html
  


class AddImageApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log += 1
            add_page_download_form = AddImageForm(request.POST, request.FILES)
            if add_page_download_form.is_valid():
                log += 1
                cd=add_page_download_form.cleaned_data
                page_id = cd['page_id']
                title = cd['title']
                image = request.FILES['image']
                
                result,message,image = ImageRepo(request=request).add_image(
                    page_id=page_id,
                    title=title,
                    image=image,
                    )
                if result==SUCCEED and image is not None:
                    context['image'] = ImageSerializer(image).data
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)
    
 
class ToggleLikeApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=1
        if request.method=='POST':
            log+=1
            add_related_page_form=TogglePageLikeForm(request.POST)
            if add_related_page_form.is_valid():
                log+=1
                page_id = add_related_page_form.cleaned_data['page_id']
                (my_like,likes_count) = LikeRepo(request=request).toggle_like(page_id=page_id)
                context['my_like'] = my_like
                context['likes_count'] = likes_count
                context['result'] = SUCCEED
        context['log']=log
        return JsonResponse(context)
        
class AddCommentApi(APIView):
    def post(self,request,*args, **kwargs):
        result,message,comment=FAILED,"",None
        context={}
        log=1
        if request.method=='POST':
            log+=1
            add_page_comment_form=AddPageCommentForm(request.POST)
            if add_page_comment_form.is_valid():
                log+=1
                page_id = add_page_comment_form.cleaned_data['page_id']
                comment = add_page_comment_form.cleaned_data['comment']
                (result,message,comment) = CommentRepo(request=request).add_comment(page_id=page_id,comment=comment)
                if result==SUCCEED:
                    context['comment'] = CommentSerializer(comment).data
        context['result'] = result
        context['message'] = message
        context['log']=log
        return JsonResponse(context)
    
           
class DeleteCommentApi(APIView):
    def post(self,request,*args, **kwargs):
        result,message,comment=FAILED,"",None
        context={}
        log=1
        if request.method=='POST':
            log+=1
            delete_page_comment_form=DeletePageCommentForm(request.POST)
            if delete_page_comment_form.is_valid():
                log+=1
                comment_id = delete_page_comment_form.cleaned_data['comment_id']
                (result,message) = CommentRepo(request=request).delete_page_comment(comment_id=comment_id)
                 
        context['result'] = result
        context['message'] = message
        context['log']=log
        return JsonResponse(context)
        
            
class AddLinkApi(APIView):
    def post(self,request,*args, **kwargs):
        result,message,comment=FAILED,"",None
        context={}
        log=1
        if request.method=='POST':
            log+=1
            add_link_form=AddLinkForm(request.POST)
            if add_link_form.is_valid():
                log+=1 
                (result,message,link) = LinkRepo(request=request).add_link(**add_link_form.cleaned_data)
                if result==SUCCEED:
                    context['link'] = LinkSerializer(link).data
        context['result'] = result
        context['message'] = message
        context['log']=log
        return JsonResponse(context)
    
       

      
class AddDownloadApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 1
        context = {}
        result,message,download=FAILED,"",None
        if request.method == 'POST':
            log += 1
            add_page_download_form = AddDownloadForm(request.POST, request.FILES)
            if add_page_download_form.is_valid():
                log += 1
                cd=add_page_download_form.cleaned_data
                page_id = cd['page_id']
                title = cd['title']
                file = request.FILES['file1']
                
                result,message,download = DownloadRepo(request=request).add_download(
                    page_id=page_id,
                    title=title,
                    file=file,
                    )
                if download is not None:
                    context['download'] = DownloadSerializer(download).data
        context['log'] = log
        context['result'] = result
        context['message'] = message
        return JsonResponse(context)
     
       