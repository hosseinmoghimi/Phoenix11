from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from utility.log import leolog
from .constants import EXCEL_PRODUCTS_DATA_START_ROW,EXCEL_SERVICES_DATA_START_ROW

from django.http import Http404,HttpResponse
from django.views import View
from .enums import *
from .forms import *
from .apps import APP_NAME
from phoenix.server_apps import phoenix_apps
from utility.excel import ReportWorkBook,get_style
from utility.calendar import PersianCalendar
from core.views import CoreContext,PageContext
from .repo import FinancialDocumentRepo,CategoryRepo
from .repo import PersonCategoryRepo,ProfileRepo,ServiceRepo,FAILED,SUCCEED,InvoiceLineItemRepo,FinancialDocumentLineRepo,AccountRepo,ProductRepo,InvoiceRepo,FinancialEventRepo,BankAccountRepo,PersonAccountRepo
from .serializers import ServiceSerializer,FinancialDocumentSerializer,CategorySerializer
from .serializers import InvoiceLineItemSerializer,AccountBriefSerializer,InvoiceLineItemUnitSerializer,InvoiceLineWithInvoiceSerializer,InvoiceLineSerializer,AccountSerializer,ProductSerializer,InvoiceSerializer,FinancialEventSerializer,FinancialDocumentLineSerializer
from .serializers import FinancialYearSerializer,ProductSpecificationSerializer,PersonAccountSerializer
from .repo import FinancialYearRepo
from utility.currency import to_price_colored
import json 
from core.views import MessageView
from .models import UnitNameEnum
LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='accounting/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"

def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
    context['WIDE_LAYOUT']=False
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context
 
def AddAccountContext(request,*args, **kwargs):
    context={}
    if request.user.has_perm(APP_NAME+".add_account"):
        context['account_natures_for_add_account']=(i[0] for i in AccountNatureEnum.choices)
        context['account_natures_for_add_person_account']=(f[0] for f in AccountNatureEnum.choices)
        context['add_account_form']=AddAccountForm()
    return context

def AddInvoiceLineItemContext(request,*args, **kwargs):
    context={}
    unit_names=(i[0] for i in UnitNameEnum.choices)
    context['unit_names_for_add_invoice_line_item']=unit_names
    return context

def AddProductContext(request,*args, **kwargs):
    context=AddInvoiceLineItemContext(request=request)
    categories=CategoryRepo(request=request).list()
    context['categories_for_add_product_app']=categories
    categories_s=json.dumps(CategorySerializer(categories,many=True).data)
    context['categories_for_add_product_app_s']=categories_s
    context['import_products_from_excel_form']=ImportProductsFromExcelForm()
    context['add_product_form']=AddProductForm()
    return context

def AddServiceContext(request):
    context=AddInvoiceLineItemContext(request=request)
    context['import_services_from_excel_form']=ImportServicesFromExcelForm()
    context['add_service_form']=AddServiceForm()
    return context

def AddInvoiceLineContext(request,*args, **kwargs):
    context={}
    unit_names=(i[0] for i in UnitNameEnum.choices)
    context["unit_names_for_add_invoice_line"]=unit_names
    context["add_invoice_line_form"]=AddInvoiceLineForm
    invoice_line_items=InvoiceLineItemRepo(request=request).list()
    invoice_line_items_s=json.dumps(InvoiceLineItemSerializer(invoice_line_items,many=True).data)
    context["invoice_line_items_s"]=invoice_line_items_s
    return context
 
def AccountsContext(request):
    context={}
    accounts=AccountRepo(request=request).list().order_by('title')
    accounts_s=json.dumps(AccountSerializer(accounts,many=True).data)
    context['accounts']=accounts
    context['accounts_s']=accounts_s
    return context

def AccountContext(request,account,*args, **kwargs):

    context={} 
    if account is None:
        return None 

        
    person_account=PersonAccountRepo(request=request).person_account(pk=account.pk)
    if person_account is not None:
        context.update(PersonContext(request=request,person=person_account.person))
        account=person_account

    bank_account=BankAccountRepo(request=request).bank_account(pk=account.pk)
    if bank_account is not None:
        context['bank_account']=bank_account
        account=bank_account
    context['account']=account
    account.normalize_total()
    account_s=json.dumps(AccountSerializer(account).data)
    context['account_s']=account_s

    
    financial_document_lines=account.financialdocumentline_set.all()

    context['financial_document_lines']=financial_document_lines
    financial_document_lines_s=json.dumps(FinancialDocumentLineSerializer(financial_document_lines,many=True).data)
    context['financial_document_lines_s']=financial_document_lines_s


 
    all_sub_accounts_lines=account.all_sub_accounts_lines().order_by('-bedehkar')
    all_sub_accounts_lines_s=json.dumps(FinancialDocumentLineSerializer(all_sub_accounts_lines,many=True).data)
    context['all_sub_accounts_lines_s']=all_sub_accounts_lines_s
    context['financial_document_lines']=all_sub_accounts_lines
    context['financial_document_lines_s']=all_sub_accounts_lines_s


    
    financial_events=FinancialEventRepo(request=request).list(account_code=account.code)
    financial_events_s=json.dumps(FinancialEventSerializer(financial_events,many=True).data)
    context['financial_events']=financial_events
    context['financial_events_s']=financial_events_s 



    accounts =account.account_set.all()
    context['accounts']=accounts
    if len(accounts)>0:
        context['expand_accounts']=True
    accounts_s=json.dumps(AccountSerializer(accounts,many=True).data)
    context['accounts_s']=accounts_s
 
    return context

def InvoiceLineItemContext(request,invoice_line_item,*args, **kwargs):
    context=PageContext(request=request,page=invoice_line_item)

    context['invoice_line_item']=invoice_line_item
    
    invoice_lines=invoice_line_item.invoiceline_set.order_by('row')
    context['invoice_lines']=invoice_lines
    invoice_lines_s=json.dumps(InvoiceLineWithInvoiceSerializer(invoice_lines,many=True).data)
    context['invoice_lines_s']=invoice_lines_s

 
    invoice_line_item_units=invoice_line_item.units.all()
    invoice_line_item_units_s=json.dumps(InvoiceLineItemUnitSerializer(invoice_line_item_units,many=True).data)
    context['invoice_line_item_units']=invoice_line_item_units
    context['invoice_line_item_units_s']=invoice_line_item_units_s
    if request.user.has_perm(APP_NAME+".add_invoicelineitemunit"):
        context.update(AddInvoiceLineItemUnitsContext(request=request,invoice_line_item=invoice_line_item))
    return context

def AddInvoiceLineItemUnitsContext(request,invoice_line_item,*args, **kwargs):
    context={}
   
    if request.user.has_perm(APP_NAME+".add_invoicelineitemunit"):
        context["add_invoice_line_item_unit_form"]=AddInvoiceLineItemUnitForm()
        context['unit_names']=(i[0] for i in UnitNameEnum.choices)
        context['base_price']=0
    return context

def FinancialEventContext(request,financial_event):
    context={}
    context['financial_event']=financial_event 
    context.update(PageContext(request=request,page=financial_event))
    
    context['financial_event']=financial_event
    financial_event_s=json.dumps(FinancialEventSerializer(financial_event).data)
    context['financial_event_s']=financial_event_s

    if request.user.has_perm(APP_NAME+'add_financialdocumentline'):
        context['add_event_financial_document_line_form']=AddEventFinancialDocumentLineForm()
        context['add_financial_document_line_form']=AddFinancialDocumentLineForm()
    
    financial_document_lines=FinancialDocumentLineRepo(request=request).list(financial_event_id=financial_event.id).order_by('-bedehkar')
    financial_document_lines_s=json.dumps(FinancialDocumentLineSerializer(financial_document_lines,many=True).data)
 
    context["financial_document_lines_s"]=financial_document_lines_s
    

    return context

def InvoiceContext(request,invoice,*args, **kwargs):
    context=FinancialEventContext(request=request,financial_event=invoice)
    context.update(AddInvoiceLineContext(request=request))
    context['invoice'] = invoice
    invoice_s=json.dumps(InvoiceSerializer(invoice).data)
    context['invoice_s'] =invoice_s

    SHOW_LINES=True
    if SHOW_LINES:
        invoice_lines=invoice.invoiceline_set.order_by('row')
        context['invoice_lines']=invoice_lines
        invoice_lines_s=json.dumps(InvoiceLineSerializer(invoice_lines,many=True).data)
        context['invoice_lines_s']=invoice_lines_s
    
    (total,discount,total_after_discount,tax,amount)=invoice.statistics
    context['total']=total
    context['total_after_discount']=total_after_discount
    context['amount']=amount
    context['discount']=discount
    context['tax']=tax
    return context
     
def ProductContext(request,product,*args, **kwargs):
    context=InvoiceLineItemContext(request=request,invoice_line_item=product)
    context['product']=product
    base_price=product.base_price
    context['base_price']=base_price

 
    
    if request.user.has_perm(APP_NAME+".change_product"):
        context['add_product_to_category_form']=AddProductToCategoryForm()
        categories=CategoryRepo(request=request).list()
        context['categories']=categories
        product_categories=product.category_set.all()
        all_product_categories=categories
        product_categories_s=json.dumps(CategorySerializer(product_categories,many=True).data)
        all_product_categories_s=json.dumps(CategorySerializer(all_product_categories,many=True).data)
        context['product_categories_s']=product_categories_s
        context['all_product_categories_s']=all_product_categories_s

    return context

def AddPersonContext(request):
    context={}
    if not request.user.has_perm(APP_NAME+".add_person"):
        return {}

    context['person_account_categories']=PersonCategoryRepo(request=request).list()
    context['add_person_form']=AddPersonForm()

    persons_ids=PersonRepo(request=request).list().values('profile_id')
    profiles=ProfileRepo(request=request).list().exclude(id__in=persons_ids)
    profiles_s=json.dumps(ProfileSerializer(profiles,many=True).data)
    context['profiles_s_for_add_person_app']=profiles_s
    context['person_prefixs']=(i[0] for i in PersonPrefixEnum.choices)
    context['person_types']=(i[0] for i in PersonTypeEnum.choices)
    context['person_types2']=(i[0] for i in PersonType2Enum.choices)
    return context
    
def PersonContext(request,person):
    context={} 
    context['person']=person
    if person.profile:
        context['profile']=person.profile
    return context

def ProductContext(request,product,*args, **kwargs):
    context={}
    context.update(InvoiceLineItemContext(request=request,invoice_line_item=product))
    context["product"]=product
    return context
 
def ServiceContext(request,service,*args, **kwargs):
    context={}
    context.update(InvoiceLineItemContext(request=request,invoice_line_item=service))
    context["service"]=service
    return context
 
    


def AddFinancialEventContext(request):
    context={}
    context['add_financial_event_form']=AddFinancialEventForm()
    return context


def AddInvoiceContext(request):
    context=AddFinancialEventContext(request=request)

    context['add_invoice_form']=AddInvoiceForm()
    return context


def AddFinancialDocumentContext(request):
    context={}
    
    if request.user.has_perm(APP_NAME+'.add_financialdocument'):
        context['add_financial_document_form']=AddFinancialDocumentForm()
        current_financial_year=FinancialYearRepo(request=request).current_financial_year()
        context['current_financial_year_id']=current_financial_year.id
        context['financial_year_statuses']=(i[0] for i in FinancialYearStatusEnum.choices)
    return context


def AddProductToCategoryContext(request,product,*args, **kwargs):
    context={}

    category_repo=CategoryRepo(request=request)
    all_categories=category_repo.list()
    all_categories_s=json.dumps(CategorySerializer(all_categories,many=True).data)
    context['all_categories_s']=all_categories_s

    
    product_categories=product.category_set.all()
    product_categories_s=json.dumps(CategorySerializer(product_categories,many=True).data)
    context['product_categories_s']=product_categories_s
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
        WAS_FOUND=False
        search_for=''   
        if search_form.is_valid():
            log=2
            search_for=search_form.cleaned_data['search_for']
            result=SUCCEED

            accounts=AccountRepo(request=request).list(search_for=search_for)
            if len(accounts)>0:
                context['accounts']=accounts
                context['accounts_s']=json.dumps(AccountSerializer(accounts,many=True).data)
                WAS_FOUND=True


                

            products=ProductRepo(request=request).list(search_for=search_for)
            if len(products)>0:
                context['products']=products
                context['products_s']=json.dumps(ProductSerializer(products,many=True).data)
                WAS_FOUND=True

                

            categories=CategoryRepo(request=request).list(search_for=search_for)
            if len(categories)>0:
                context['categories']=categories
                context['categories_s']=json.dumps(CategorySerializer(categories,many=True).data)
                WAS_FOUND=True

        context['WAS_FOUND']=WAS_FOUND
        context['search_for']=search_for
        context['message']=message
        context['log']=log
        context['result']=result
        return render(request,TEMPLATE_ROOT+"search.html",context)


class SettingsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        # accounts =AccountRepo(request=request).roots(*args, **kwargs)
        # context['accounts']=accounts
        return render(request,TEMPLATE_ROOT+"settings.html",context) 


class InvoiceToExcelView(View):
    def get(self,request,*args, **kwargs):
        now=PersianCalendar().date
        invoice=InvoiceRepo(request=request).invoice(*args, **kwargs)
        if invoice is None:
            mv=MessageView(request=request)
            mv.title="فاکتور پیدا نشد."
            mv.body="فاکتور پیدا نشد."
            return mv.response()
        date=PersianCalendar().from_gregorian(now)
        lines=[]
        for i,invoice_line in enumerate(invoice.invoiceline_set.all(),start=1):
            line={
                'row':i,
                'title':invoice_line.invoice_line_item.title,
                'quantity':str(invoice_line.quantity) + invoice_line.unit_name,      
                'discount':invoice_line.discount,      
                'unit_price':invoice_line.unit_price,      
                'line_total':invoice_line.line_total,      
            }
            lines.append(line)
        headers=['ردیف',
                 'عنوان',
                 'تعداد', 
                 'تخفیف',
                 'فی',
                 'مبلغ'
        ]
        report_work_book=ReportWorkBook()
        report_work_book=ReportWorkBook(origin_file_name=f'Invoice.xlsx')
        style=get_style(font_name='B Koodak',size=12,bold=False,color='FF000000',start_color='FFFFFF',end_color='FF000000')
        # sheet1=ReportSheet(
        #     data=lines,
        #     start_row=3,
        #     start_col=1,
        #     table_has_header=False,
        #     table_headers=None,
        #     style=style,
        #     sheet_name='links',
            
        # )
        
        start_row=3
        report_work_book.add_sheet(
            data=lines,
            start_row=start_row,
            table_has_header=False,
            table_headers=headers,
            style=style,
            sheet_name='Invoice',
        )
            
        file_name=f"""Phoenix Invoice {invoice.pk} {date.replace('/','').replace(':','')}.xlsx"""
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response.AppendHeader("Content-Type", "application/vnd.ms-excel");
        response["Content-disposition"]=f"attachment; filename={file_name}"
        report_work_book.work_book.save(response)
        report_work_book.work_book.close()
        return response


class FinancialYearsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_years=FinancialYearRepo(request=request).list(*args, **kwargs)
        context['expand_financial_years']=True
        context['financial_years']=financial_years
        financial_years_s=json.dumps(FinancialYearSerializer(financial_years,many=True).data)
        context['financial_years_s']=financial_years_s
        if request.user.has_perm(APP_NAME+".add_financialyear"):
            context['add_financial_year_form']=AddFinancialYearForm()
            context['add_financial_year_form_statuses']=(i[0] for i in FinancialYearStatusEnum.choices)
            context['default_status']=FinancialYearStatusEnum.DRAFT
        return render(request,TEMPLATE_ROOT+"financial-years.html",context)


class FinancialYearView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_year=FinancialYearRepo(request=request).financial_year(*args, **kwargs)
        context['WIDE_LAYOUT']=True
        if financial_year is None:
            from core.views import MessageView
            mv=MessageView()
            context={}
            back_url = request.META.get('HTTP_REFERER')
            context['back_url'] = back_url
            context["title"]="سال مالی وجود ندارد."
            context["body"]="چنین سال مالی وجود ندارد."
            return mv.get(request=request,**context)

        context['financial_year']=financial_year
        
        accounting_documents=AccountingDocumentRepo(request=request).list(financial_year_id=financial_year.id)
        context['accounting_documents']=accounting_documents
        accounting_documents_s=json.dumps(AccountingDocumentSerializer(accounting_documents,many=True).data)
        context['accounting_documents_s']=accounting_documents_s

        return render(request,TEMPLATE_ROOT+"financial-year.html",context)


class TreeChartView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context[WIDE_LAYOUT]=True
        
        context=getContext(request=request)
        if 'pk' in kwargs and not int(kwargs["pk"])==0:
            account=AccountRepo(request=request).account(*args, **kwargs)

            accounts=account.all_childs()
            context['account']=account
        else:
            accounts=AccountRepo(request=request).list(*args, **kwargs)

        context['accounts']=accounts
        pages=[]
         
        AG=100
        BA=100000
        MA=100000000
        MA2=10000000000
        for account in accounts:
            pages.append({
                'title': f"""{account.code}<br>{account.name}""",
                'parent_id': account.parent_id,
                'parent': 0,
                'get_absolute_url': account.get_absolute_url(),
                'id': account.id,
                'pre_title': "",
                'color': account.color,
                'sub_title':to_price_colored(account.balance),
                })

        context['pages_s'] = json.dumps(pages)
        return render(request,TEMPLATE_ROOT+"tree-chart.html",context) 


class TreeListView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        accounts =AccountRepo(request=request).roots(*args, **kwargs)
        context['accounts']=accounts
        context[WIDE_LAYOUT]=True
        return render(request,TEMPLATE_ROOT+"tree-list.html",context) 


class FinancialDocumentView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_document=FinancialDocumentRepo(request=request).financial_document(*args, **kwargs)
        context['financial_document']=financial_document
        financial_document_s=json.dumps(FinancialDocumentSerializer(financial_document).data)
        context['financial_document_s']=financial_document_s

        
        financial_document_lines=financial_document.financialdocumentline_set.all()

        context['financial_document_lines']=financial_document_lines
        financial_document_lines_s=json.dumps(FinancialDocumentLineSerializer(financial_document_lines,many=True).data)
        context['financial_document_lines_s']=financial_document_lines_s

        if request.user.has_perm(APP_NAME+'.add_financialdocumentline'):
            context['add_financial_document_line_form']=AddFinancialDocumentLineForm()

             

        return render(request,TEMPLATE_ROOT+"financial-document.html",context)


class FinancialDocumentsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_documents=FinancialDocumentRepo(request=request).list()
        context['financial_documents']=financial_documents
        financial_documents_s=json.dumps(FinancialDocumentSerializer(financial_documents,many=True).data)
        context['financial_documents_s']=financial_documents_s
 
        context.update(AddFinancialDocumentContext(request=request))
        return render(request,TEMPLATE_ROOT+"financial-documents.html",context)


class FinancialDocumentLineView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        financial_document_line=FinancialDocumentLineRepo(request=request).financial_document_line(*args, **kwargs)
        context['financial_document_line']=financial_document_line

        context.update(PageContext(request=request,page=financial_document_line))

        return render(request,TEMPLATE_ROOT+"financial-document-line.html",context)


class AccountsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        
        accounts=AccountRepo(request=request).list(*args, **kwargs)

        context['accounts']=accounts
        accounts_s=json.dumps(AccountSerializer(accounts,many=True).data)
        context['accounts_s']=accounts_s
        context.update(AddAccountContext(request=request))
        return render(request,TEMPLATE_ROOT+"accounts.html",context)


class AccountView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        account=AccountRepo(request=request).account(*args, **kwargs)


        if account is None:
            raise Http404
        context.update(AccountContext(request=request,account=account))
        
        if request.user.has_perm(APP_NAME+".add_financialdocumentline"):
            context['add_financial_document_line_form']=AddFinancialDocumentLineForm()
 
        if request.user.has_perm(APP_NAME+".add_account"):
            context.update(AddAccountContext(request=request))
         

        return render(request,TEMPLATE_ROOT+"account.html",context)


class SelectionView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)

        account_groups=AccountRepo(request=request).list(level=0,*args, **kwargs)
        context['account_groups']=account_groups
        account_groups_s=json.dumps(AccountBriefSerializer(account_groups,many=True).data)
        context['account_groups_s']=account_groups_s

        

        basic_accounts=AccountRepo(request=request).list(level=1,*args, **kwargs)
        context['basic_accounts']=basic_accounts
        basic_accounts_s=json.dumps(AccountBriefSerializer(basic_accounts,many=True).data)
        context['basic_accounts_s']=basic_accounts_s


        moein_accounts=AccountRepo(request=request).list(level=2,*args, **kwargs)
        context['moein_accounts']=moein_accounts
        moein_accounts_s=json.dumps(AccountBriefSerializer(moein_accounts,many=True).data)
        context['moein_accounts_s']=moein_accounts_s

         
        moein2_accounts=AccountRepo(request=request).list(level=3,*args, **kwargs)
        context['moein2_accounts']=moein2_accounts
        moein2_accounts_s=json.dumps(AccountBriefSerializer(moein2_accounts,many=True).data)
        context['moein2_accounts_s']=moein2_accounts_s


        context['WIDE_LAYOUT']=True
        return render(request,TEMPLATE_ROOT+"selection.html",context)


class ProductsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        products =ProductRepo(request=request).list(*args, **kwargs)
        context['products']=products
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s

        if request.user.has_perm(APP_NAME+".add_product"):
            context.update(AddProductContext(request=request)) 
        context[WIDE_LAYOUT]=True
        return render(request,TEMPLATE_ROOT+"products.html",context) 
 

class InvoiceLineItemView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        invoice_line_item=InvoiceLineItemRepo(request=request).invoice_line_item(*args, **kwargs)
        if invoice_line_item is None:
            raise Http404
        

        context.update(InvoiceLineItemContext(request=request,invoice_line_item=invoice_line_item))

        context['phoenix_apps']=phoenix_apps
        return render(request,TEMPLATE_ROOT+"invoice-line-item.html",context)
       
    
class ProductView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        product=ProductRepo(request=request).product(*args, **kwargs)
        if product is None:
            raise Http404
        

        context.update(ProductContext(request=request,product=product))
        context.update(AddProductToCategoryContext(request=request,product=product))


        product_specifications=product.productspecification_set.all()
        product_specifications_s=json.dumps(ProductSpecificationSerializer(product_specifications,many=True).data)
        context['product_specifications']=product_specifications
        context['product_specifications_s']=product_specifications_s
        if request.user.has_perm(APP_NAME+".add_productspecification"):
            context["add_product_specification_form"]=AddProductSpecificationForm()
            specification_names=['رنگ','وزن','اندازه','جرم','نوع','حجم',]
            context['specification_names']=specification_names
     

        return render(request,TEMPLATE_ROOT+"product.html",context)
    

class InvoiceLineView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        product=ProductRepo(request=request).product(*args, **kwargs)
        if product is None:
            raise Http404
        

        context.update(ProductContext(request=request,product=product))

        context['phoenix_apps']=phoenix_apps
        return render(request,TEMPLATE_ROOT+"invoice-line.html",context)
    
    
class ServiceView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        service=ServiceRepo(request=request).service(*args, **kwargs)
        if service is None:
            raise Http404
        

        context.update(ServiceContext(request=request,service=service))

        return render(request,TEMPLATE_ROOT+"service.html",context)   


class ServicesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        services=ServiceRepo(request=request).list(*args, **kwargs)
        services_s=json.dumps(ServiceSerializer(services,many=True).data)
        context['services']=services
        context['services_s']=services_s
        if request.user.has_perm(APP_NAME+'.add_service'):
            context.update(AddServiceContext(request=request))
        return render(request,TEMPLATE_ROOT+"services.html",context)


class ExportProductsToExcelView(View):   
    def get(self,request,*args, **kwargs):
        now=PersianCalendar().date
        
        data=[]  
        headers=["id","title","barcode","unit_name","unit_price","thumbnail"]
        
        products=ProductRepo(request=request).list()
         
            
        
        date=PersianCalendar().from_gregorian(now)
        lines=[]
        for i,product in enumerate(products,start=1):
            line={
                'row':i,
                'title':product.title,
                'barcode':product.barcode,      
                'unit_name':product.unit_name,      
                'unit_price':product.unit_price,       
            }
            lines.append(line)
        headers=['ردیف',
                 'عنوان',
                 'بارکد', 
                 'واحد',
                 'فی',
        ]
        report_work_book=ReportWorkBook()
        report_work_book=ReportWorkBook(origin_file_name=f'products.xlsx')
        style=get_style(font_name='B Koodak',size=12,bold=False,color='FF000000',start_color='FFFFFF',end_color='FF000000')
        # sheet1=ReportSheet(
        #     data=lines,
        #     start_row=3,
        #     start_col=1,
        #     table_has_header=False,
        #     table_headers=None,
        #     style=style,
        #     sheet_name='links',
            
        # )
        
        start_row=EXCEL_PRODUCTS_DATA_START_ROW
        if start_row>2:
            start_row-=1
        report_work_book.add_sheet(
            data=lines,
            start_row=start_row,
            table_has_header=False,
            table_headers=headers,
            style=style,
            sheet_name='products',
        )
            
        file_name=f"""Phoenix Products {date.replace('/','').replace(':','')}.xlsx"""
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response.AppendHeader("Content-Type", "application/vnd.ms-excel");
        response["Content-disposition"]=f"attachment; filename={file_name}"
        report_work_book.work_book.save(response)
        report_work_book.work_book.close()
        return response


class ExportServicesToExcelView(View):
  
    def get(self,request,*args, **kwargs):
        now=PersianCalendar().date
        
        data=[]  
        headers=["id","title","barcode","unit_name","unit_price","thumbnail"]
        
        services=ServiceRepo(request=request).list()
         
            
        
        date=PersianCalendar().from_gregorian(now)
        lines=[]
        for i,service in enumerate(services,start=1):
            line={
                'row':i,
                'title':service.title,
                'unit_name':service.unit_name,      
                'unit_price':service.unit_price,       
            }
            lines.append(line)
        headers=['ردیف',
                 'عنوان',
                 'واحد',
                 'فی',
        ]
        report_work_book=ReportWorkBook()
        report_work_book=ReportWorkBook(origin_file_name=f'services.xlsx')
        style=get_style(font_name='B Koodak',size=12,bold=False,color='FF000000',start_color='FFFFFF',end_color='FF000000')
        # sheet1=ReportSheet(
        #     data=lines,
        #     start_row=3,
        #     start_col=1,
        #     table_has_header=False,
        #     table_headers=None,
        #     style=style,
        #     sheet_name='links',
            
        # )
        
        start_row=EXCEL_SERVICES_DATA_START_ROW
        if start_row>2:
            start_row-=1
        report_work_book.add_sheet(
            data=lines,
            start_row=start_row,
            table_has_header=False,
            table_headers=headers,
            style=style,
            sheet_name='services',
        )
            
        file_name=f"""Phoenix Services {date.replace('/','').replace(':','')}.xlsx"""
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response.AppendHeader("Content-Type", "application/vnd.ms-excel");
        response["Content-disposition"]=f"attachment; filename={file_name}"
        report_work_book.work_book.save(response)
        report_work_book.work_book.close()
        return response
 

class FinancialEventView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_event=FinancialEventRepo(request=request).financial_event(*args, **kwargs)
        context.update(FinancialEventContext(request=request,financial_event=financial_event))
        context['financial_event']=financial_event
        context['WIDE_LAYOUT']=True 
        return render(request,TEMPLATE_ROOT+"financial-event.html",context)


class FinancialEventsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_events=FinancialEventRepo(request=request).list()
        financial_events_s=json.dumps(FinancialEventSerializer(financial_events,many=True).data)
        context['financial_events']=financial_events
        context['financial_events_s']=financial_events_s
        context['WIDE_LAYOUT']=True
        if request.user.has_perm(APP_NAME+'.add_financialevnt'):
            context.update(AddFinancialEventContext(request=request))
        return render(request,TEMPLATE_ROOT+"financial-events.html",context)


class AddFinancialEventView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        invoices=InvoiceRepo(request=request).list()
        invoices_s=json.dumps(InvoiceSerializer(invoices,many=True).data)
        context['invoices']=invoices
        context['invoices_s']=invoices_s
        context['WIDE_LAYOUT']=True
        return render(request,TEMPLATE_ROOT+"add-finanical-event.html",context)

    def post(self,request,*args, **kwargs):
        from .apis import AddFinancialEventApi
        return AddFinancialEventApi().post(request=request)


class InvoicesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        invoices=InvoiceRepo(request=request).list()
        invoices_s=json.dumps(InvoiceSerializer(invoices,many=True).data)
        context['invoices']=invoices
        context['invoices_s']=invoices_s
        context['WIDE_LAYOUT']=True
        if request.user.has_perm(APP_NAME+".add_invoice"):
            context.update(AddInvoiceContext(request=request))
        return render(request,TEMPLATE_ROOT+"invoices.html",context)


class InvoiceView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        invoice=InvoiceRepo(request=request).invoice(*args, **kwargs)
        context['invoice']=invoice
        invoice_s=json.dumps(InvoiceSerializer(invoice,many=False).data)
        context['invoice_s']=invoice_s
        context.update(InvoiceContext(request=request,invoice=invoice))

        
        # if True:
            # invoice_line_items=InvoiceLineItemRepo(request=request).list()
            # context.update(AddInvoiceLineContext(request=request))
            # invoice_line_items_s=json.dumps(InvoiceLineItemSerializer(invoice_line_items,many=True).data)
            # context["invoice_line_items_s"]=invoice_line_items_s

        return render(request,TEMPLATE_ROOT+"invoice.html",context)


class InvoicePrintView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        invoice=InvoiceRepo(request=request).invoice(*args, **kwargs)
        context['invoice']=invoice
        context['NOT_REPONSIVE']=True
        context['NOT_NAVBAR']=True
        context['WIDE_LAYOUT']=True
        context['NOT_FOOTER']=True
        invoice_s=json.dumps(InvoiceSerializer(invoice,many=False).data)
        context['invoice_s']=invoice_s
        context.update(InvoiceContext(request=request,invoice=invoice))
        return render(request,TEMPLATE_ROOT+"invoice-print.html",context)


class CategoryView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        category_repo=CategoryRepo(request=request)
        category=category_repo.category(*args, **kwargs)
        context['category']=category
        category_s=json.dumps(CategorySerializer(category,many=False).data)
        context['category_s']=category_s 


        if category is None:
            categories=category_repo.roots()
            context['category_id']=0
            products=[]
        else:
            categories=category_repo.list(parent_id=category.id)
            products=category.products.all()
            context['category_id']=category.id
            # leolog(all_childs_products=category.all_childs_products())

        context['categories']=categories
        categories_s=json.dumps(CategorySerializer(categories,many=True).data)
        context['categories_s']=categories_s



        context['products']=products
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s

        if request.user.has_perm(APP_NAME+'.add_category'):
            context['add_category_form']=AddCategoryForm()
        if request.user.has_perm(APP_NAME+'.add_product'):
            context['add_product_form']=AddProductForm()
            context.update(AddProductContext(request=request))
        return render(request,TEMPLATE_ROOT+"category.html",context)


class CategoriesView(View):
    def get(self,request,*args, **kwargs):
        return CategoryView().get(request=request,pk=0)
        context=getContext(request=request)
        categories=CategoryRepo(request=request).list(*args, **kwargs)
        context['categories']=categories
        categories_s=json.dumps(CategorySerializer(categories,many=True).data)
        context['categories_s']=categories_s
        return render(request,TEMPLATE_ROOT+"categories.html",context)




class PersonAccountsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
       
        person_accounts=PersonAccountRepo(request=request).list(*args, **kwargs)

        context['person_accounts']=person_accounts
        person_accounts_s=json.dumps(PersonAccountSerializer(person_accounts,many=True).data)
        context['person_accounts_s']=person_accounts_s

        
        if request.user.has_perm(APP_NAME+'.add_personaccount'):
            context.update(AddAccountContext(request=request))
            person_categories=PersonCategoryRepo(request=request).list()
            context['person_categories']=person_categories
            context['add_person_account_form']=AddPersonAccountForm()
        return render(request,TEMPLATE_ROOT+"person-accounts.html",context)


class PersonAccountView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        person_account=PersonAccountRepo(request=request).person_account(*args, **kwargs)


        if person_account is None:
            raise Http404
        context.update(AccountContext(request=request,account=person_account))
        
        if request.user.has_perm(APP_NAME+".add_financialdocumentline"):
            context['add_financial_document_line_form']=AddFinancialDocumentLineForm()
  
        return render(request,TEMPLATE_ROOT+"person-account.html",context)
