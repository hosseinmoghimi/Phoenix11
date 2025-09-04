from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from .repo import DrugRepo,PatientRepo,DoctorRepo,PrescriptionRepo
from .serializers import DrugSerializer,DoctorSerializer,PatientSerializer,PrescriptionSerializer
from django.views import View
from .forms import *
from .apps import APP_NAME
from core.views import CoreContext,PageContext
from utility.calendar import PersianCalendar
import json
from utility.enums import UnitNameEnum
from utility.log import leolog
from accounting.views import AddProductContext,ProductContext,InvoiceContext
LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='health/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"
 
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context


def DrugContext(request,drug,*args, **kwargs):
    context=PageContext(request=request,page=drug)
    return context
 
 
class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        return render(request,TEMPLATE_ROOT+"index.html",context)
# Create your views here. 

 
 
class DrugsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        drugs=DrugRepo(request=request).list(*args, **kwargs)
        context["drugs"]=drugs
        drugs_s=json.dumps(DrugSerializer(drugs,many=True).data)
        context["drugs_s"]=drugs_s
        if request.user.has_perm(APP_NAME+'.add_drug'):
            context['add_drug_form']=AddDrugForm()
            context.update(AddProductContext(request=request))
        return render(request,TEMPLATE_ROOT+"drugs.html",context)
# Create your views here. 




 
class DrugView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        drug=DrugRepo(request=request).drug(*args, **kwargs)
        context["drug"]=drug
        context.update(ProductContext(request=request,product=drug))
        return render(request,TEMPLATE_ROOT+"drug.html",context)
# Create your views here. 



# Create your tests here.

class DoctorsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        doctors=DoctorRepo(request=request).list(*args, **kwargs)
        context["doctors"]=doctors
        doctors_s=json.dumps(DoctorSerializer(doctors,many=True).data)
        context["doctors_s"]=doctors_s
        if request.user.has_perm(APP_NAME+'.add_doctor'):
            context['add_doctor_form']=AddDoctorForm()
            context.update(AddProductContext(request=request))
        return render(request,TEMPLATE_ROOT+"doctors.html",context)
# Create your views here. 




 
class DoctorView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        doctor=DoctorRepo(request=request).doctor(*args, **kwargs)
        context["doctor"]=doctor
        doctor_s=json.dumps(DoctorSerializer(doctor).data)
        context["doctor_s"]=doctor_s
        return render(request,TEMPLATE_ROOT+"doctor.html",context)
# Create your views here. 



class PatientsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        patients=PatientRepo(request=request).list(*args, **kwargs)
        context["patients"]=patients
        patients_s=json.dumps(PatientSerializer(patients,many=True).data)
        context["patients_s"]=patients_s
        if request.user.has_perm(APP_NAME+'.add_patient'):
            context['add_patient_form']=AddPatientForm()
            context.update(AddProductContext(request=request))
        return render(request,TEMPLATE_ROOT+"patients.html",context)
# Create your views here. 




 
class PatientView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        patient=PatientRepo(request=request).patient(*args, **kwargs)
        context["patient"]=patient
        patient_s=json.dumps(PatientSerializer(patient).data)
        context["patient_s"]=patient_s
        return render(request,TEMPLATE_ROOT+"patient.html",context)
# Create your views here. 

 
 
class PrescriptionsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        prescriptions=PrescriptionRepo(request=request).list(*args, **kwargs)
        context["prescriptions"]=prescriptions
        prescriptions_s=json.dumps(PrescriptionSerializer(prescriptions,many=True).data)
        context["prescriptions_s"]=prescriptions_s
        if request.user.has_perm(APP_NAME+'.add_prescription'):
            context['add_prescription_form']=AddPrescriptionForm()
            context.update(AddProductContext(request=request))
        return render(request,TEMPLATE_ROOT+"prescriptions.html",context)
# Create your views here. 


from accounting.views import FinancialEventStatusEnum,AddInvoiceLineContext,InvoiceLineItemRepo,AddInvoiceLineForm,InvoiceLineItemSerializer
from django.db.models import Q


def AddPrescriptionLineContext(request,*args, **kwargs):
    context=AddInvoiceLineContext(request=request)
    unit_names=(i[0] for i in UnitNameEnum.choices)
    context["unit_names_for_add_invoice_line"]=unit_names
    context["unit_names_for_edit_invoice_line"]=unit_names
    unit_names2=[]
    for ii in UnitNameEnum.choices:
        unit_names2.append(str(ii[0]))
    context["unit_names_for_edit_invoice_line_s"]=json.dumps(unit_names2)
    context["add_invoice_line_form"]=AddInvoiceLineForm
    invoice_line_items=InvoiceLineItemRepo(request=request).list().filter(Q(class_name='drug')|Q(class_name='service'))
    invoice_line_items_s=json.dumps(InvoiceLineItemSerializer(invoice_line_items,many=True).data)
    context["invoice_line_items_s"]=invoice_line_items_s
    return context

def PrescriptionContext(request,prescription,*args, **kwargs):
    invoice=prescription
    context=InvoiceContext(request=request,invoice=invoice,warehouse=True) 

    if invoice.status==FinancialEventStatusEnum.APPROVED:
        pass
    elif invoice.status==FinancialEventStatusEnum.DELIVERED:
        pass
    elif invoice.status==FinancialEventStatusEnum.FINISHED: 
        pass 
    else:
        context.update(AddPrescriptionLineContext(request=request))

    return context


class PrescriptionView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        prescription=PrescriptionRepo(request=request).prescription(*args, **kwargs)
        context["prescription"]=prescription
        prescription_s=json.dumps(PrescriptionSerializer(prescription).data)
        context["prescription_s"]=prescription_s

        context.update(PrescriptionContext(request=request,prescription=prescription,warehouse=True))

        


        return render(request,TEMPLATE_ROOT+"prescription.html",context)
# Create your views here. 
