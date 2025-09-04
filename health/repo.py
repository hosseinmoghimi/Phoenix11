from .models import Drug,Doctor,Patient,Prescription,PrescriptionLine
from .apps import APP_NAME
from .enums import * 
from django.db.models import Q 
from authentication.repo import PersonRepo 
from utility.num import filter_number
from utility.calendar import PersianCalendar
from utility.constants import FAILED,SUCCEED
from utility.log import leolog
from .enums import *

 

class DrugRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Drug.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=Drug.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        if "meal_id" in kwargs:
            meal_id=kwargs["meal_id"]
            objects=objects.filter(meal_id=meal_id)  
        return objects.all()
        
    def drug(self,*args, **kwargs):
        if "drug_id" in kwargs and kwargs["drug_id"] is not None:
            return self.objects.filter(pk=kwargs['drug_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_drug(self,*args,**kwargs):
        result,message,drug=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_drug"):
            message="دسترسی غیر مجاز"
            return result,message,drug
         
        drug=Drug()

        if 'barcode' in kwargs:
            drug.barcode=kwargs["barcode"]
        if 'priority' in kwargs and kwargs['priority'] is not None:
            drug.priority=kwargs["priority"]
        if 'title' in kwargs:
            drug.title=kwargs["title"]

          
 
        (result,message,drug)=drug.save()

        
        if 'unit_price' in kwargs:
            if 'unit_name' in kwargs:
                if 'coef' in kwargs:
                    from accounting.models import InvoiceLineItemUnit
                    ili_unit=InvoiceLineItemUnit()
                    ili_unit.unit_name=kwargs["unit_name"]
                    ili_unit.coef=kwargs["coef"]
                    ili_unit.unit_price=kwargs["unit_price"]
                    ili_unit.invoice_line_item_id=drug.id
                    ili_unit.default=True
                    ili_unit.save()

        return result,message,drug

 
class DoctorRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Doctor.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=Doctor.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def doctor(self,*args, **kwargs):
        if "doctor_id" in kwargs and kwargs["doctor_id"] is not None:
            return self.objects.filter(pk=kwargs['doctor_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_doctor(self,*args,**kwargs):
        result,message,doctor=FAILED,"",None 
        if len(Doctor.objects.filter(person_account_id=kwargs["person_account_id"]))>0:
            message='حساب تکراری برای دکتر جدید'
            return FAILED,message,None
        if not self.request.user.has_perm(APP_NAME+".add_doctor"):
            message="دسترسی غیر مجاز"
            return result,message,doctor

        doctor=Doctor() 
        if 'person_account_id' in kwargs:
            doctor.person_account_id=kwargs["person_account_id"]
        if 'name' in kwargs:
            doctor.name=kwargs["name"]
          
        (result,message,doctor)=doctor.save()
        return result,message,doctor

 
class PatientRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Patient.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=Patient.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def patient(self,*args, **kwargs):
        if "patient_id" in kwargs and kwargs["patient_id"] is not None:
            return self.objects.filter(pk=kwargs['patient_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_patient(self,*args,**kwargs):
        result,message,patient=FAILED,"",None 
        if len(Patient.objects.filter(person_account_id=kwargs["person_account_id"]))>0:
            message='حساب تکراری برای بیمار جدید'
            return FAILED,message,None
        if not self.request.user.has_perm(APP_NAME+".add_patient"):
            message="دسترسی غیر مجاز"
            return result,message,patient

        patient=Patient() 
        if 'person_account_id' in kwargs:
            patient.person_account_id=kwargs["person_account_id"]
        if 'name' in kwargs:
            patient.name=kwargs["name"]
          
        (result,message,patient)=patient.save()
        return result,message,patient

 

class PrescriptionRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Prescription.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=Prescription.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        if "meal_id" in kwargs:
            meal_id=kwargs["meal_id"]
            objects=objects.filter(meal_id=meal_id)  
        return objects.all()
        
    def prescription(self,*args, **kwargs):
        if "prescription_id" in kwargs and kwargs["prescription_id"] is not None:
            return self.objects.filter(pk=kwargs['prescription_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_prescription(self,*args,**kwargs):
        result,message,prescription=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_prescription"):
            message="دسترسی غیر مجاز"
            return result,message,prescription
         
        prescription=Prescription()

        if 'barcode' in kwargs:
            prescription.barcode=kwargs["barcode"]
        if 'priority' in kwargs and kwargs['priority'] is not None:
            prescription.priority=kwargs["priority"]
        if 'title' in kwargs:
            prescription.title=kwargs["title"]

          
 
        (result,message,prescription)=prescription.save()

        
        if 'unit_price' in kwargs:
            if 'unit_name' in kwargs:
                if 'coef' in kwargs:
                    from accounting.models import InvoiceLineItemUnit
                    ili_unit=InvoiceLineItemUnit()
                    ili_unit.unit_name=kwargs["unit_name"]
                    ili_unit.coef=kwargs["coef"]
                    ili_unit.unit_price=kwargs["unit_price"]
                    ili_unit.invoice_line_item_id=prescription.id
                    ili_unit.default=True
                    ili_unit.save()

        return result,message,prescription

 