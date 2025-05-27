
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import ProductRepo,AccountRepo
from .serializers import  ProductSerializer
from django.http import JsonResponse
from .forms import *
 


class ImportProductsFromExcelApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            ImportProductsFromExcelForm_=ImportProductsFromExcelForm(request.POST,request.FILES)
            if ImportProductsFromExcelForm_.is_valid():
                log=333
                
                excel_file = request.FILES['file1']
                cd=ImportProductsFromExcelForm_.cleaned_data
                cd['excel_file']=excel_file
                result,message,products=ProductRepo(request=request).import_products_from_excel(**cd)
                if products is not None:
                    context['products']=ProductSerializer(products,many=True).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)

 
class AddProductApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
        add_product_form=AddProductForm(request.POST)
        if add_product_form.is_valid():
            log=333
            cd=add_product_form.cleaned_data
            result,message,product=ProductRepo(request=request).add_product(**cd)
            if product is not None:
                context['product']=ProductSerializer(product).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 