
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import MenuRepo,ShopRepo
from .serializers import MenuSerializer,ShopSerializer,SupplierSerializer,CustomerSerializer
from django.http import JsonResponse
from .forms import *
   

class AddMenuApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
        add_menu_form=AddMenuForm(request.POST)
        if add_menu_form.is_valid():
            log=333
            cd=add_menu_form.cleaned_data
            result,message,menu=MenuRepo(request=request).add_menu(**cd)
            if menu is not None:
                context['menu']=MenuSerializer(menu).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
  

  
class AddShopApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
        add_shop_form=AddShopForm(request.POST)
        if add_shop_form.is_valid():
            log=333
            cd=add_shop_form.cleaned_data
            result,message,shop=ShopRepo(request=request).add_shop(**cd)
            if shop is not None:
                context['shop']=ShopSerializer(shop).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
  