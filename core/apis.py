# from core.serializers import PageBriefSerializer, PageCommentSerializer, PageDecodeSerializer, PageDownloadSerializer, PageImageSerializer, PageLikeSerializer, PageLinkSerializer, PagePermissionSerializer, PageSerializer, PageTagSerializer, ParameterSerializer, TagSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from .forms import *
# from .repo import ContactMessageRepo, PageCommentRepo, PageLinkRepo, PagePermissionRepo, PageRepo, PageTagRepo,  ParameterRepo,PageDownloadRepo,PageImageRepo
from .repo import  PageRepo 
from .serializer import  PageSerializer
from utility.constants import SUCCEED, FAILED
from utility.utils import str_to_html
  


    
class SetPageThumbnailHeaderApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log += 1
            SetThumbnailHeaderForm_ = SetPageThumbnailHeaderForm(request.POST, request.FILES)
            if SetThumbnailHeaderForm_.is_valid():
                log += 1
                cd=SetThumbnailHeaderForm_.cleaned_data
                page_id = cd['page_id']
                clear_thumbnail = cd['clear_thumbnail']
                clear_header = cd['clear_header']
                thumbnail = None
                header = None
                if 'thumbnail' in request.FILES:
                    thumbnail = request.FILES['thumbnail']
                if 'header' in request.FILES:
                    header = request.FILES['header']
                
                page = PageRepo(request=request).set_thumbnail_header(
                    clear_thumbnail=clear_thumbnail,
                    clear_header=clear_header,
                    page_id=page_id,
                    thumbnail=thumbnail,
                    header=header
                    )
                if page is not None:
                    context['page'] = PageSerializer(page).data
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)

class TogglePageLikeApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=1
        if request.method=='POST':
            log+=1
            add_related_page_form=TogglePageLikeForm(request.POST)
            if add_related_page_form.is_valid():
                log+=1
                page_id = add_related_page_form.cleaned_data['page_id']
                (my_like,likes_count) = PageRepo(request=request).toggle_like(page_id=page_id)
                context['my_like'] = my_like
                context['likes_count'] = likes_count
                context['result'] = SUCCEED
        context['log']=log
        return JsonResponse(context)
        