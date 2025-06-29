
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import InvoiceRepo,InvoiceLineRepo,InvoiceLineItemUnitRepo,ProductRepo,AccountRepo,PersonRepo,BankRepo,PersonCategoryRepo,AccountingDocumentLineRepo,AccountingDocumentRepo,FinancialEventRepo,PersonAccountRepo
from .serializers import  InvoiceSerializer,InvoiceLineItemUnitSerializer,ProductSerializer,AccountSerializer,InvoiceLineSerializer
from django.http import JsonResponse
from .forms import *
 

class AddInvoiceApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
        add_invoice_form=AddInvoiceForm(request.POST)
        if add_invoice_form.is_valid():
            log=333
            cd=add_invoice_form.cleaned_data
            result,message,invoice=InvoiceRepo(request=request).add_invoice(**cd)
            if invoice is not None:
                context['invoice']=InvoiceSerializer(invoice).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)

class AddAccountApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        add_account_form=AddAccountForm(request.POST)
        if add_account_form.is_valid():
            cd=add_account_form.cleaned_data
            (result,message,account)=AccountRepo(request=request).add_account(**cd) 
            if result==SUCCEED:
                context["account"]=AccountSerializer(account).data
            # (result2,message2)=PersonRepo(request=request).initial_default_persons() 
        context['message']=message
        context['result']=result
        # context['message2']=message2
        # context['result2']=result2
        context['log']=log
        return JsonResponse(context)

class SetAccountPriorityApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            set_account_priority_form=SetAccountPriorityForm(request.POST)
            if set_account_priority_form.is_valid():
                log=333
                cd=set_account_priority_form.cleaned_data
                priority,message,result=AccountRepo(request=request).set_priority(**cd)
                if priority is not None:
                    context['priority']=priority
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)

class SetAccountParentApi(APIView): 
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        action=None
        log=111
        context['result']=FAILED
        set_parent_code_form=SetParentCodeForm(request.POST)
        if set_parent_code_form.is_valid():
            log=2222
            cd=set_parent_code_form.cleaned_data
            (result,message,account,parent)=AccountRepo(request=request).set_account_parent(**cd) 
            if result==SUCCEED:
                log=333 
                context["parent"]=AccountSerializer(parent,many=False).data 
                context["account"]=AccountSerializer(account,many=False).data 
        context['message']=message
        context['result']=result 
        context['log']=log
        return JsonResponse(context)


class AddInvoiceLineItemUnitApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            add_invoice_line_item_unit_form=AddInvoiceLineItemUnitForm(request.POST)
            if add_invoice_line_item_unit_form.is_valid():
                log=333
                cd=add_invoice_line_item_unit_form.cleaned_data 
                result,message,invoice_line_item_unit=InvoiceLineItemUnitRepo(request=request).add_invoice_line_item_unit(**cd)
                if invoice_line_item_unit is not None:
                    context['invoice_line_item_unit']=InvoiceLineItemUnitSerializer(invoice_line_item_unit).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
    
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

class AddInvoiceLineApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            add_invoice_line_form=AddInvoiceLineForm(request.POST)
            if add_invoice_line_form.is_valid():
                log=333
                cd=add_invoice_line_form.cleaned_data 
                result,message,invoice_line=InvoiceLineRepo(request=request).add_invoice_line(**cd)
                if invoice_line is not None:
                    context['invoice_line']=InvoiceLineSerializer(invoice_line).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
    
 
class SelectAccountApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            select_account_form=SelectAccountForm(request.POST)
            if select_account_form.is_valid():
                log=333
                cd=select_account_form.cleaned_data
                account=AccountRepo(request=request).account(**cd)
                if account is not None:
                    result=SUCCEED
                    message="موفقیت آمیز"
                    context['account']=AccountSerializer(account).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class InitALLAccountsApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            (result1,message1)=AccountRepo(request=request).initial_default_accounts() 
            (result2,message2)=PersonCategoryRepo(request=request).initial_default_person_categories()
            (result3,message3)=BankRepo(request=request).initial_default_banks() 
        context['message1']=message1
        context['result1']=result1
        context['message2']=message2
        context['result2']=result2
        context['message3']=message3
        context['result3']=result3
        context['log']=log
        return JsonResponse(context)


class DeleteALLAccountsApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            (result3,message3)=AccountingDocumentLineRepo(request=request).delete_all() 
            (result3,message3)=FinancialEventRepo(request=request).delete_all() 
            (result3,message3)=PersonRepo(request=request).delete_all() 
            (result3,message3)=PersonAccountRepo(request=request).delete_all() 
            (result,message)=AccountRepo(request=request).delete_all_accounts() 
            (result2,message2)=PersonCategoryRepo(request=request).delete_all() 
            (result2,message2)=BankRepo(request=request).delete_all() 
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
 