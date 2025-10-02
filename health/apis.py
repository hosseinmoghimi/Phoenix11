
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import DrugRepo,DoctorRepo,PatientRepo,PrescriptionRepo
from .serializers import DrugSerializer,PatientSerializer,DoctorSerializer,PrescriptionSerializer
from django.http import JsonResponse
from .forms import *
   


class AddDrugApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_drug_form=AddDrugForm(request.POST)
        if add_drug_form.is_valid():
            log=333
            cd=add_drug_form.cleaned_data
            result,message,drug=DrugRepo(request=request).add_drug(**cd)
            if drug is not None:
                context['drug']=DrugSerializer(drug).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 

 
class AddPrescriptionApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_drug_form=AddPrescriptionForm(request.POST)
        if add_drug_form.is_valid():
            log=333
            cd=add_drug_form.cleaned_data
            result,message,drug=PrescriptionRepo(request=request).add_drug(**cd)
            if drug is not None:
                context['drug']=PrescriptionSerializer(drug).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 
 
class AddDoctorApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_doctor_form=AddDoctorForm(request.POST)
        if add_doctor_form.is_valid():
            log=333
            cd=add_doctor_form.cleaned_data
            result,message,doctor=DoctorRepo(request=request).add_doctor(**cd)
            if doctor is not None:
                context['doctor']=DoctorSerializer(doctor).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 

 
class AddPatientApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_patient_form=AddPatientForm(request.POST)
        if add_patient_form.is_valid():
            log=333
            cd=add_patient_form.cleaned_data
            result,message,patient=PatientRepo(request=request).add_patient(**cd)
            if patient is not None:
                context['patient']=PatientSerializer(patient).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 