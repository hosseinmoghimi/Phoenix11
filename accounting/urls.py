from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),
    path('selection/',login_required(views.SelectionView.as_view()),name="selection"),
    path('settings/',login_required(views.SettingsView.as_view()),name="settings"),
    path('products/',login_required(views.ProductsView.as_view()),name="products"),
    path('invoices/',login_required(views.InvoicesView.as_view()),name="invoices"),
    path('invoice/<int:pk>/',login_required(views.InvoiceView.as_view()),name="invoice"),
    path('invoice/print/<int:pk>/',login_required(views.InvoicePrintView.as_view()),name="invoice_print"),
    path('invoice_line/<int:pk>/',login_required(views.InvoiceLineView.as_view()),name="invoiceline"),
    path('product/<int:pk>/',login_required(views.ProductView.as_view()),name="product"),
    path('export-products-to-excel/',login_required(views.ExportProductsToExcelView.as_view()),name="export_products_to_excel"),
    path('services/',login_required(views.ServicesView.as_view()),name="services"),
    path("add-product/",login_required(apis.AddProductApi.as_view()),name="add_product"),
    path('account/<int:pk>/',login_required(views.AccountView.as_view()),name="account"),
    path('service/<int:pk>/',login_required(views.ServiceView.as_view()),name="service"),
    
    path("add-product-unit/",login_required(apis.AddProductUnitApi.as_view()),name="add_product_unit"),

      
    path("events/",login_required(views.EventsView.as_view()),name="events"),
    path("add-event/",login_required(views.AddEventView.as_view()),name="add_event"),
    
    path("select-account/",login_required(apis.SelectAccountApi.as_view()),name="select_account"),
    
    path("init_all_accounts/",login_required(apis.InitALLAccountsApi.as_view()),name="init_all_accounts"),
    path("delete_all_accounts/",login_required(apis.DeleteALLAccountsApi.as_view()),name="delete_all_accounts"),


    path('accounts/',login_required(views.AccountsView.as_view()),name="accounts"),
    path("import-products-from-excel/",login_required(apis.ImportProductsFromExcelApi.as_view()),name="import_products_from_excel"),
    path("tree-chart/<int:pk>/",login_required(views.TreeChartView.as_view()),name="tree_chart"),
    path("tree-list/",login_required(views.TreeListView.as_view()),name="tree_list"),
   

]
