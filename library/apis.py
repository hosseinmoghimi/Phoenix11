
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import BookRepo
from .serializers import BookSerializer
 
from django.http import JsonResponse
from .forms import *
   
 
class AddBookApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
        add_book_form=AddBookForm(request.POST)
        if add_book_form.is_valid():
            log=333
            cd=add_book_form.cleaned_data
            result,message,book=BookRepo(request=request).add_book(**cd)
            if result==SUCCEED:
                context['book']=BookSerializer(book).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
   