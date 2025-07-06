from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),
    path('search/',login_required(views.SearchView.as_view()),name="search"),

    path("tree-chart/<int:pk>/",login_required(views.TreeChartView.as_view()),name="tree_chart"),
    path("tree-list/",login_required(views.TreeListView.as_view()),name="tree_list"),
    path('settings/',login_required(views.SettingsView.as_view()),name="settings"),

    path("init_all_accounts/",login_required(apis.InitALLAccountsApi.as_view()),name="init_all_accounts"),
    path("delete_all_accounts/",login_required(apis.DeleteALLAccountsApi.as_view()),name="delete_all_accounts"),
    
    path('accounts/',login_required(views.AccountsView.as_view()),name="accounts"),
    path('account/<int:pk>/',login_required(views.AccountView.as_view()),name="account"),
    path("add-account/",login_required(apis.AddAccountApi.as_view()),name="add_account"),
    path('selection/',login_required(views.SelectionView.as_view()),name="selection"),
    path("select-account/",login_required(apis.SelectAccountApi.as_view()),name="select_account"),
    path("set-account-priority/",login_required(apis.SetAccountPriorityApi.as_view()),name="set_account_priority"),
    path("set_account_parent/",login_required(apis.SetAccountParentApi.as_view()),name="set_account_parent"),

    path('financialdocuments/',login_required(views.FinancialDocumentsView.as_view()),name="financial_documents"),
    path('financial-document/<int:pk>/',login_required(views.FinancialDocumentView.as_view()),name="financialdocument"),
    path("select-financial-document/",login_required(apis.SelectFinancialDocumentApi.as_view()),name="select_financial_document"),
    
    path('financial-document-line/<int:pk>/',login_required(views.FinancialDocumentLineView.as_view()),name="financialdocumentline"),
    path('add-financial-document-line/',login_required(apis.AddFinancialDocumentLineApi.as_view()),name="add_financial_document_line"),
    
    path('products/',login_required(views.ProductsView.as_view()),name="products"),
    path('product/<int:pk>/',login_required(views.ProductView.as_view()),name="product"),
    path("add-product/",login_required(apis.AddProductApi.as_view()),name="add_product"),
    path('export-products-to-excel/',login_required(views.ExportProductsToExcelView.as_view()),name="export_products_to_excel"),
    path("import-products-from-excel/",login_required(apis.ImportProductsFromExcelApi.as_view()),name="import_products_from_excel"),
    
    path('invoices/',login_required(views.InvoicesView.as_view()),name="invoices"),
    path('invoice/<int:pk>/',login_required(views.InvoiceView.as_view()),name="invoice"),
    path('invoice/excel/<int:pk>/',login_required(views.InvoiceToExcelView.as_view()),name="invoice_to_excel"),
    path('invoice-line-item/<int:pk>/',login_required(views.InvoiceLineItemView.as_view()),name="invoicelineitem"),
    path('invoice/print/<int:pk>/',login_required(views.InvoicePrintView.as_view()),name="invoice_print"),
    path('invoice_line/<int:pk>/',login_required(views.InvoiceLineView.as_view()),name="invoiceline"),
    
    path('services/',login_required(views.ServicesView.as_view()),name="services"),
    path('service/<int:pk>/',login_required(views.ServiceView.as_view()),name="service"),
    path("add-service/",login_required(apis.AddServiceApi.as_view()),name="add_service"),
    path('export-services-to-excel/',login_required(views.ExportServicesToExcelView.as_view()),name="export_services_to_excel"),
    path("import-services-from-excel/",login_required(apis.ImportServicesFromExcelApi.as_view()),name="import_services_from_excel"),
    
    path('add-invoice/',login_required(apis.AddInvoiceApi.as_view()),name="add_invoice"),
    path("add-invoice-line/",login_required(apis.AddInvoiceLineApi.as_view()),name="add_invoice_line"),
    
    path("add-invoice-line-item-unit/",login_required(apis.AddInvoiceLineItemUnitApi.as_view()),name="add_invoice_line_item_unit"),

      
    path("financial_events/",login_required(views.FinancialEventsView.as_view()),name="financial_events"),
    path("financial_event/<int:pk>/",login_required(views.FinancialEventView.as_view()),name="financialevent"),
    path("add-financial-event/",login_required(views.AddFinancialEventView.as_view()),name="add_financial_event"),
    path("add-financial-event-post/",login_required(apis.AddFinancialEventApi.as_view()),name="add_financial_event_post"),
    path("select-financial-event/",login_required(apis.SelectFinancialEventApi.as_view()),name="select_financial_event"),
    
    


   

    
]
