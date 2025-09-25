from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from .repo import WareHouseRepo,WareHouseSheetRepo,WareHouseSheetSignatureRepo,WareHouseSheetLabelRepo
from .serializers import WareHouseSheetLabelSerializer,WareHouseSerializer,WareHouseSheetSerializer,WareHouseSheetSignatureSerializer
from django.views import View
from organization.views import OrganizationUnitRepo,OrganizationUnitSerializer

from utility.enums import *
from .enums import *
from .forms import *
from .apps import APP_NAME
from core.views import CoreContext
from phoenix.server_apps import phoenix_apps
from utility.calendar import PersianCalendar
from organization.views import OrganizationUnitRepo,OrganizationUnitSerializer
import json
from utility.enums import UnitNameEnum
from utility.log import leolog
from accounting.views import AddInvoiceLineContext,InvoiceContext,ProductContext
LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='warehouse/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"
 
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context

 
def SearchContext(request,search_for,*args, **kwargs):
    context={}
    WAS_FOUND=False

    warehouses=WareHouseRepo(request=request).list(search_for=search_for)
    if len(warehouses)>0:
        context['warehouses']=warehouses
        context['warehouses_s']=json.dumps(WareHouseSerializer(warehouses,many=True).data)
        WAS_FOUND=True


          

    context['WAS_FOUND']=WAS_FOUND
    return context

 
def AddWareHouseSheetContext(request):
    context={}
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
 
 
class WareHousesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        warehouses=WareHouseRepo(request=request).list(*args, **kwargs)
        context["warehouses"]=warehouses
        warehouses_s=json.dumps(WareHouseSerializer(warehouses,many=True).data)
        context["warehouses_s"]=warehouses_s
        if request.user.has_perm(APP_NAME+'.add_warehouse'):
            context['add_warehouse_form']=AddWareHouseForm()
            organization_units = OrganizationUnitRepo(request=request).list(*args, **kwargs)

            context['organization_units']=organization_units
            organization_units_s=json.dumps(OrganizationUnitSerializer(organization_units,many=True).data)
            context['organization_units_s']=organization_units_s
        return render(request,TEMPLATE_ROOT+"warehouses.html",context)

 
class AddMaterialRequestView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        context["WIDE_LAYOUT"]=True
        context.update(AddInvoiceLineContext(request=request))


        warehouses=WareHouseRepo(request=request).list(*args, **kwargs)
        context["warehouses"]=warehouses
        warehouses_s=json.dumps(WareHouseSerializer(warehouses,many=True).data)
        context["warehouses_s"]=warehouses_s


        organization_units=OrganizationUnitRepo(request=request).list(*args, **kwargs)
        context["organization_units"]=organization_units
        organization_units_s=json.dumps(OrganizationUnitSerializer(organization_units,many=True).data)
        context["organization_units_s"]=organization_units_s


        warehouse_sheets=WareHouseSheetRepo(request=request).list(*args, **kwargs).filter(invoice_line__invoice_id=None)
        context["warehouse_sheets"]=warehouse_sheets
        warehouse_sheets_s=json.dumps(WareHouseSheetSerializer(warehouse_sheets,many=True).data)
        context["warehouse_sheets_s"]=warehouse_sheets_s

        from accounting.views import InvoiceLineRepo,InvoiceLineSerializer
        invoice_lines=InvoiceLineRepo(request=request).list(*args, **kwargs).filter(invoice_id=None)
        context["invoice_lines"]=invoice_lines
        invoice_lines_s=json.dumps(InvoiceLineSerializer(invoice_lines,many=True).data)
        context["invoice_lines_s"]=invoice_lines_s
  
        return render(request,TEMPLATE_ROOT+"add-material-request.html",context)
    def post(self,request,*args, **kwargs):
        from .apis import AddMaterialRequestApi
        return AddMaterialRequestApi().post(request=request)


class WareHouseView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        context["WIDE_LAYOUT"]=True

        warehouse=WareHouseRepo(request=request).warehouse(*args, **kwargs)
        context["warehouse"]=warehouse
        warehouse_s=json.dumps(WareHouseSerializer(warehouse,many=False).data)
        context["warehouse_s"]=warehouse_s

        
        warehouse_sheets=WareHouseSheetRepo(request=request).list(warehouse_id=warehouse.id)
        context["warehouses"]=warehouse_sheets
        warehouse_sheets_s=json.dumps(WareHouseSheetSerializer(warehouse_sheets,many=True).data)
        context["warehouse_sheets_s"]=warehouse_sheets_s


        return render(request,TEMPLATE_ROOT+"warehouse.html",context)

 
class WareHouseSheetLabelsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        warehouse_sheet_labels=WareHouseSheetLabelRepo(request=request).list(*args, **kwargs)
        context["WIDE_LAYOUT"]=True

        context["warehouse_sheet_labels"]=warehouse_sheet_labels
        warehouse_sheet_labels_s=json.dumps(WareHouseSheetLabelSerializer(warehouse_sheet_labels,many=True).data)
        context["warehouse_sheet_labels_s"]=warehouse_sheet_labels_s
        
        return render(request,TEMPLATE_ROOT+"warehouse-sheet-labels.html",context)
   
 
class WareHouseSheetLabelView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        warehouse_sheet_label=WareHouseSheetLabelRepo(request=request).warehouse_sheet_label(*args, **kwargs)
        context["warehouse_sheet_label"]=warehouse_sheet_label
        warehouse_sheet_label_s=json.dumps(WareHouseSheetSerializer(warehouse_sheet_label,many=False).data)
        context["warehouse_sheet_label_s"]=warehouse_sheet_label_s
        return render(request,TEMPLATE_ROOT+"warehouse-sheet-label.html",context)

 
class WareHouseSheetsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        warehouse_sheets=WareHouseSheetRepo(request=request).list(*args, **kwargs)
        context["WIDE_LAYOUT"]=True
        context["warehouses"]=warehouse_sheets
        warehouse_sheets_s=json.dumps(WareHouseSheetSerializer(warehouse_sheets,many=True).data)
        context["warehouse_sheets_s"]=warehouse_sheets_s
        if request.user.has_perm(APP_NAME+'.add_warehouse'):
            context['add_warehouse_sheet_form']=AddWareHouseSheetForm()
            organization_units = OrganizationUnitRepo(request=request).list(*args, **kwargs)

            context['organization_units']=organization_units
            organization_units_s=json.dumps(OrganizationUnitSerializer(organization_units,many=True).data)
            context['organization_units_s']=organization_units_s
        return render(request,TEMPLATE_ROOT+"warehouse-sheets.html",context)
   
 
class WareHouseSheetView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        warehouse_sheet=WareHouseSheetRepo(request=request).warehouse_sheet(*args, **kwargs)
        context["warehouse_sheet"]=warehouse_sheet
        warehouse_sheet_s=json.dumps(WareHouseSheetSerializer(warehouse_sheet,many=False).data)
        context["warehouse_sheet_s"]=warehouse_sheet_s

        warehouse_sheet_signatures=WareHouseSheetSignatureRepo(request=request).list(warehouse_sheet_id=warehouse_sheet.id,*args, **kwargs)
        context["warehouse_sheet_signatures"]=warehouse_sheet_signatures
        warehouse_sheet_signatures_s=json.dumps(WareHouseSheetSignatureSerializer(warehouse_sheet_signatures,many=True).data)
        context["warehouse_sheet_signatures_s"]=warehouse_sheet_signatures_s



        warehouse_sheet_labels=WareHouseSheetLabelRepo(request=request).list(warehouse_sheet_id=warehouse_sheet.id,*args, **kwargs)
        context["warehouse_sheet_labels"]=warehouse_sheet_labels
        warehouse_sheet_labels_s=json.dumps(WareHouseSheetLabelSerializer(warehouse_sheet_labels,many=True).data)
        context["warehouse_sheet_labels_s"]=warehouse_sheet_labels_s


        from organization.views import EmployeeRepo,EmployeeSerializer
        me_employee=EmployeeRepo(request=request).me
        
        if me_employee is not None:
            context['me_employee']=me_employee
            me_employee_s=json.dumps(EmployeeSerializer(me_employee).data)
            context['me_employee_s']=me_employee_s
            context['warehouse_sheet_signature_statuses']=(i[0] for i in SignatureStatusEnum.choices)
            context['add_warehouse_sheet_signature_form']=AddWareHouseSheetSignatureForm()
        if me_employee is not None:
            context['me_employee']=me_employee
            me_employee_s=json.dumps(EmployeeSerializer(me_employee).data)
            context['me_employee_s']=me_employee_s
            context['add_warehouse_sheet_label_form']=AddWareHouseSheetLabelForm()
        return render(request,TEMPLATE_ROOT+"warehouse-sheet.html",context)


 