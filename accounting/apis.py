
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from .repo import CategoryRepo,BankRepo,PersonCategoryRepo,FinancialDocumentLineRepo,FinancialDocumentRepo,FinancialEventRepo,PersonAccountRepo,BrandRepo
from .repo import ServiceRepo,InvoiceRepo,InvoiceLineRepo,InvoiceLineItemUnitRepo,ProductRepo,AccountRepo
from utility.log import leolog
from .serializers import  InvoiceLineItemUnitBriefSerializer, ServiceSerializer,FinancialDocumentSerializer,FinancialEventSerializer,FinancialDocumentLineSerializer
from .serializers import CategorySerializer,InvoiceSerializer,InvoiceLineItemUnitSerializer,ProductSerializer,AccountSerializer,InvoiceLineSerializer,BrandSerializer
from django.http import JsonResponse
from .forms import *
from .repo import FinancialYearRepo,ProductSpecificationRepo,PersonAccountRepo
from .serializers import FinancialYearSerializer,ProductSpecificationSerializer,PersonAccountSerializer
 
class AddProductToCategoryApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
        add_product_to_category_form=AddProductToCategoryForm(request.POST)
        if add_product_to_category_form.is_valid():
            log=333
            cd=add_product_to_category_form.cleaned_data
            result,message,product_categories=CategoryRepo(request=request).add_product_to_category(**cd)
            if result==SUCCEED:
                context['product_categories']=CategorySerializer(product_categories,many=True).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class AddPersonAccountApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
        add_person_account_form=AddPersonAccountForm(request.POST)
        if add_person_account_form.is_valid():
            log=333
            cd=add_person_account_form.cleaned_data
            result,message,person_account=PersonAccountRepo(request=request).add_person_account(**cd)
            if result==SUCCEED:
                context['person_account']=PersonAccountSerializer(person_account,many=False).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)

class AddProductSpecificationApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            add_product_specification_form=AddProductSpecificationForm(request.POST)
            if add_product_specification_form.is_valid():
                log=333
                cd=add_product_specification_form.cleaned_data 
                result,message,product_specification,deleted_id=ProductSpecificationRepo(request=request).add_product_specification(**cd)
                if product_specification is not None:
                    context['product_specification']=ProductSpecificationSerializer(product_specification).data
                    context['deleted_id']=deleted_id
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)




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


class AddFinancialDocumentLineApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
        add_financial_document_line_form=AddFinancialDocumentLineForm(request.POST)
        if add_financial_document_line_form.is_valid():
            log=333
            cd=add_financial_document_line_form.cleaned_data
            result,message,financial_document_line=FinancialDocumentLineRepo(request=request).add_financial_document_line(**cd)
            if financial_document_line is not None:

                context['financial_document_line']=FinancialDocumentLineSerializer(financial_document_line).data
                if cd['financial_document_id']==0:
                 context['financial_document']=FinancialDocumentSerializer(financial_document_line.financial_document).data
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
                result,message,invoice_line_item_units=InvoiceLineItemUnitRepo(request=request).add_invoice_line_item_unit(**cd)
                if invoice_line_item_units is not None:
                    context['invoice_line_item_units']=InvoiceLineItemUnitSerializer(invoice_line_item_units,many=True).data
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


class ImportServicesFromExcelApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            ImportServicesFromExcelForm_=ImportServicesFromExcelForm(request.POST,request.FILES)
            if ImportServicesFromExcelForm_.is_valid():
                log=333
                
                excel_file = request.FILES['file1']
                cd=ImportServicesFromExcelForm_.cleaned_data
                cd['excel_file']=excel_file
                result,message,services=ServiceRepo(request=request).import_services_from_excel(**cd)
                if services is not None:
                    context['services']=ServiceSerializer(services,many=True).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class AddFinancialEventApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            add_financial_event_form=AddFinancialEventForm(request.POST,request.FILES)
            if add_financial_event_form.is_valid():
                log=333
                 
                cd=add_financial_event_form.cleaned_data
                result,message,financial_event=FinancialEventRepo(request=request).add_financial_event(**cd)
                if financial_event is not None:
                    context['financial_event']=FinancialEventSerializer(financial_event,many=False).data
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


 
class AddFinancialYearApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        add_financial_year_form=AddFinancialYearForm(request.POST)
        if add_financial_year_form.is_valid():
            cd=add_financial_year_form.cleaned_data
            (result,message,financial_year,financial_years)=FinancialYearRepo(request=request).add_financial_year(**cd) 
            if result==SUCCEED:
                context["financial_years"]=FinancialYearSerializer(financial_years,many=True).data
                context["financial_year"]=FinancialYearSerializer(financial_year).data
            # (result2,message2)=PersonRepo(request=request).initial_default_persons() 
        context['message']=message
        context['result']=result
        # context['message2']=message2
        # context['result2']=result2
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



class GetInvoiceLineItemUnitsApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            get_invoice_line_item_units_form=GetInvoiceLineItemUnitsForm(request.POST)
            if get_invoice_line_item_units_form.is_valid():
                log=333
                cd=get_invoice_line_item_units_form.cleaned_data 
                invoice_line_item_units=InvoiceLineItemUnitRepo(request=request).list(**cd)
                if invoice_line_item_units is not None:
                    context['invoice_line_item_units']=InvoiceLineItemUnitBriefSerializer(invoice_line_item_units,many=True).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)



class SelectFinancialEventApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            select_financial_event_form=SelectFinancialEventForm(request.POST)
            if select_financial_event_form.is_valid():
                log=333
                cd=select_financial_event_form.cleaned_data
                financial_event=FinancialEventRepo(request=request).financial_event(**cd)
                if financial_event is not None:
                    result=SUCCEED
                    message="موفقیت آمیز"
                    context['financial_event']=FinancialEventSerializer(financial_event).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class SelectFinancialDocumentApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            select_financial_document_form=SelectFinancialDocumentForm(request.POST)
            if select_financial_document_form.is_valid():
                log=333
                cd=select_financial_document_form.cleaned_data
                financial_document=FinancialDocumentRepo(request=request).financial_document(**cd)
                if financial_document is not None:
                    result=SUCCEED
                    message="موفقیت آمیز"
                    context['financial_document']=FinancialDocumentSerializer(financial_document).data
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


class SelectPersonAccountApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            select_person_account_form=SelectPersonAccountForm(request.POST)
            if select_person_account_form.is_valid():
                log=333
                cd=select_person_account_form.cleaned_data
                person_account=PersonAccountRepo(request=request).person_account(**cd)
                if person_account is not None:
                    result=SUCCEED
                    message="موفقیت آمیز"
                    context['person_account']=PersonAccountSerializer(person_account).data
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
            from authentication.repo import PersonRepo
            (result2,message2)=PersonCategoryRepo(request=request).delete_all() 
            (result3,message3)=PersonRepo(request=request).delete_all() 
            (result3,message3)=FinancialDocumentLineRepo(request=request).delete_all() 
            (result3,message3)=FinancialEventRepo(request=request).delete_all() 
            (result3,message3)=PersonAccountRepo(request=request).delete_all() 
            (result,message)=AccountRepo(request=request).delete_all_accounts() 
            (result2,message2)=BankRepo(request=request).delete_all() 
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class AddBrandApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
        add_brand_form=AddBrandForm(request.POST)
        if add_brand_form.is_valid():
            log=333
            cd=add_brand_form.cleaned_data
            result,message,brand=BrandRepo(request=request).add_brand(**cd)
            if brand is not None:
                context['brand']=BrandSerializer(brand).data
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

 

class AddServiceApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        message="پارامتر های ورودی صحیح نمی باشند."
        add_service_form=AddServiceForm(request.POST)
        if add_service_form.is_valid():
            log=333
            cd=add_service_form.cleaned_data
            result,message,service=ServiceRepo(request=request).add_service(**cd)
            if service is not None:
                context['service']=ServiceSerializer(service).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 

class AddCategoryApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        add_category_form=AddCategoryForm(request.POST)
        if add_category_form.is_valid():
            log=333
            cd=add_category_form.cleaned_data
            result,message,category=CategoryRepo(request=request).add_category(**cd)
            if category is not None:
                context['category']=CategorySerializer(category).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 