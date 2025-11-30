
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import CatalogRepo
from .serializers import CatalogSerializer
 
from django.http import JsonResponse
from .forms import *
   
 
class AddCatalogApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_catalog_form=AddCatalogForm(request.POST)
        if add_catalog_form.is_valid():
            log=333
            cd=add_catalog_form.cleaned_data
            result,message,catalog=CatalogRepo(request=request).add_catalog(**cd)
            if result==SUCCEED:
                context['catalog']=CatalogSerializer(catalog).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
   