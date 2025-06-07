from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL,CURRENCY
from authentication.repo import ProfileRepo
from django.views import View
from .forms import *
from .apps import APP_NAME
from phoenix.server_apps import phoenix_apps
from utility.calendar import PersianCalendar
from utility.log import leolog

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

    current_date=persian_date.to_date()
    current_datetime=persian_date.to_datetime() 

    context['current_datetime']=current_datetime
    context['current_date']=current_date

    context['phoenix_apps']=phoenix_apps
    
    # parameter_repo=ParameterRepo(request=request,app_name=app_name)
    # context['farsi_font_name']=parameter_repo.parameter(name="نام فونت فارسی",default="Vazir").value
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
    profile=ProfileRepo(request=request).me
    context.update(PageLikesContext(request=request,page=page,profile=profile))
     
    return context

def PageLikesContext(request,page,profile):
    context={}
    likes_count=5
    my_like = page.my_like(profile=profile)
    context['my_like']=my_like
    context['likes_count']=likes_count  
    if profile is not None:
        context['toggle_page_like_form']=TogglePageLikeForm()
    context['page']=page
    return context



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
