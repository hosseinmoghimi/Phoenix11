from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL,CURRENCY,VUE_VERSION_3,VUE_VERSION_2
from authentication.repo import ProfileRepo
from utility.repo import ParameterRepo,PictureRepo
from django.views import View
from .enums import *
from .forms import *
from .repo import PageRepo
from .apps import APP_NAME
from phoenix.server_apps import phoenix_apps
from utility.calendar import PersianCalendar
from utility.log import leolog
from utility.views import MessageView
from django.utils import timezone
import json
from .repo import PageRepo,FAILED,SUCCEED
from .serializer import PageSerializer,PageBriefSerializer

LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='core/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"


def CoreContext(request,*args, **kwargs):
    context={}
    app_name='core'
    if 'app_name' in kwargs:
        app_name=kwargs['app_name']
    context['APP_NAME']=app_name
    context['VUE_VERSION_3']=VUE_VERSION_3
    context['VUE_VERSION_2']=VUE_VERSION_2
    context['DEBUG']=DEBUG
    me_profile=ProfileRepo(request=request).me
    if me_profile is not None:
        context['me_profile']=me_profile
        context['profile']=me_profile
    context['ADMIN_URL']=ADMIN_URL
    context['SITE_URL']=SITE_URL
    context['STATIC_URL']=STATIC_URL
    context['SITE_URL']=SITE_URL
    
    context['CURRENCY']=CURRENCY
    persian_date=PersianCalendar() 
    now=timezone.now()
    current_datetime=persian_date.from_gregorian(now) 
    current_date=current_datetime[0:10]

    context['current_datetime']=current_datetime
    context['current_date']=current_date
    current_time=current_datetime[10:]
    context['current_time']=current_time

    context['phoenix_apps']=phoenix_apps
    parameter_repo=ParameterRepo(request=request,app_name=app_name)
    context['farsi_font_name']=parameter_repo.parameter(name=PARAMETER_NAME_ENUM.FARSI_FONT,default="Tanha").value
    # app_has_background=parameter_repo.parameter(name=ParameterNameEnum.HAS_APP_BACKGROUND,default=False).boolean_value
    # app_background_image=PictureRepo(request=request,app_name=app_name).picture(name=PictureNameEnum.APP_BACKGROUND_IMAGE)
    # if app_has_background:
    #     context['app_background_image']=app_background_image

    for appp in phoenix_apps:
        if appp['name']==app_name:
            # context['current_app']={'name':appp['name'],'title':appp['title'],'url':appp['url'],'logo':appp['logo']}
            context['current_app']=appp
            context['app_title']=appp['title']
 
    return context

        
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context

def PageContext(request,page,*args, **kwargs):
    context={}
    context['page']=page
    me_profile=ProfileRepo(request=request).me
    from attachments.views import PageTagsContext,PageLocationsContext,PageImagesContext,PageRelatedContext,PageLikesContext,PageCommentsContext,PageLinksContext,PageDownloadsContext

    context.update(PageLikesContext(request=request,page=page,profile=me_profile))
    context.update(PageCommentsContext(request=request,page=page,profile=me_profile))
    context.update(PageLinksContext(request=request,page=page,profile=me_profile))
    context.update(PageDownloadsContext(request=request,page=page,profile=me_profile))
    context.update(PageImagesContext(request=request,page=page,profile=me_profile))
    context.update(PageRelatedContext(request=request,page=page,profile=me_profile))
    context.update(PageLocationsContext(request=request,page=page,profile=me_profile))
    context.update(PageTagsContext(request=request,page=page,profile=me_profile))
    return context



class SearchView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps 
         
        return render(request,TEMPLATE_ROOT+"search.html",context)

    def post(self,request,*args, **kwargs):
        result=FAILED
        message=''
        log=1
        context=getContext(request=request) 
        search_form=SearchForm(request.POST)
        if search_form.is_valid():
            log=2
            search_for=search_form.cleaned_data['search_for']
            pages=PageRepo(request=request).list(search_for=search_for)
            result=SUCCEED

            context['pages']=pages
            context['pages_s']=json.dumps(PageSerializer(pages,many=True).data)

        context['message']=message
        context['log']=log
        context['result']=result
        return render(request,TEMPLATE_ROOT+"search.html",context)



class PageView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        page=PageRepo(request=request).page(*args, **kwargs)
        if page is None:
            mv=MessageView()
            return mv.get(request=request)
        context.update(PageContext(request=request,page=page))
        return render(request,TEMPLATE_ROOT+"page.html",context)
# Create your views here.

class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        phoenix_apps = sorted(phoenix_apps, key=lambda d: d['priority'])

        context['phoenix_apps']=phoenix_apps
        return render(request,TEMPLATE_ROOT+"index.html",context)
# Create your views here.
