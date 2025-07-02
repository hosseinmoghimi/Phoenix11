from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from accounting.repo import ProductRepo
from accounting.serializers import ProductSerializer
from .serializers import MenuSerializer,SupplierSerializer
from .repo import MenuRepo,SupplierRepo
from .forms import *
from .apps import APP_NAME
from phoenix.server_apps import phoenix_apps
from utility.calendar import PersianCalendar
import json
from django.views import View


LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='market/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"


def CoreContext(app_name,request,*args, **kwargs):
    context={}
    context['APP_NAME']=app_name
    context['DEBUG']=DEBUG
    # me_profile=ProfileRepo(request=request).me
    # if me_profile is not None:
    #     context['me_profile']=me_profile
        # context['profile']=me_profile
    context['ADMIN_URL']=ADMIN_URL
    context['SITE_URL']=SITE_URL
    context['STATIC_URL']=STATIC_URL
    
    persian_date=PersianCalendar() 
    from django.utils import timezone
    Now=timezone.now()
    current_date=persian_date.from_gregorian(Now)
    current_datetime=persian_date.from_gregorian(Now) 

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

 

class ProductsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        products =ProductRepo(request=request).list(*args, **kwargs)
        context['products']=products
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s
 
        context[WIDE_LAYOUT]=True
        return render(request,TEMPLATE_ROOT+"products.html",context) 
    
    

    
class ProductView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        product =ProductRepo(request=request).list(*args, **kwargs)
        context['product']=product
        product_s=json.dumps(ProductSerializer(product,many=True).data)
        context['product_s']=product_s
        context[WIDE_LAYOUT]=True
        return render(request,TEMPLATE_ROOT+"product.html",context) 
    

class MenusView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        menus =MenuRepo(request=request).list(*args, **kwargs)
        context['menus']=menus
        menus_s=json.dumps(MenuSerializer(menus,many=True).data)
        context['menus_s']=menus_s
 
        context[WIDE_LAYOUT]=True
        if request.user.has_perm(APP_NAME+".add_menu"):
            context['add_menu_form']=AddMenuForm()
            suppliers=SupplierRepo(request=request).list()
            context['suppliers']=suppliers
        return render(request,TEMPLATE_ROOT+"menus.html",context) 
    
    

    
class MenuView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        menu =MenuRepo(request=request).menu(*args, **kwargs)
        context['menu']=menu
        menu_s=json.dumps(MenuSerializer(menu,many=False).data)
        context['menu_s']=menu_s
 
        context[WIDE_LAYOUT]=True
        return render(request,TEMPLATE_ROOT+"menu.html",context) 
    
    

