from django.db import models
from core.models import _,reverse,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from phoenix.server_settings import CURRENCY
from .apps import APP_NAME
from accounting.models import Product,Invoice,InvoiceLine
 

class Drug(Product,LinkHelper):
    
    app_name=APP_NAME
    class_name="drug"

    class Meta:
        verbose_name = _("Drug")
        verbose_name_plural = _("Drugs")
 
   
    def save(self):
        (result,message,drug)=FAILED,'',self
        if self.class_name is None or self.class_name=="":
            self.class_name="drug"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(Drug,self).save()
        result=SUCCEED
        message="دارو با موفقیت اضافه شد."
        return (result,message,drug)
  
class Patient(models.Model,LinkHelper):
    person_account=models.ForeignKey("accounting.personaccount", verbose_name=_("person_account"), on_delete=models.PROTECT)
    
    class_name="patient"
    app_name=APP_NAME
    class Meta:
        verbose_name = _("بیمار")
        verbose_name_plural = _("بیماران")

    def __str__(self):
        return self.person_account.person.full_name 

    def save(self,*args, **kwargs):
        result=FAILED
        message=''
        patient=None

        super(Patient,self).save()
        patient=self
        message='بیمار ذخیره شد.'
        result=SUCCEED
        return result,message,patient
    
    @property
    def last_name(self):
        return self.person_account.person.last_name
    @property
    def first_name(self):
        return self.person_account.person.first_name
    @property
    def image(self):
        return self.person_account.person.image
    
    @property
    def melli_code(self):
        return self.person_account.person.melli_code
    @property
    def father_name(self):
        return self.person_account.person.father_name
   
class Doctor(models.Model,LinkHelper):
    person_account=models.ForeignKey("accounting.personaccount", verbose_name=_("person_account"), on_delete=models.PROTECT)
    
    class_name="doctor"
    app_name=APP_NAME
    class Meta:
        verbose_name = _("دکتر")
        verbose_name_plural = _("دکتر ها")

    def __str__(self):
        return self.person_account.person.full_name 

    def save(self,*args, **kwargs):
        result=FAILED
        message=''
        doctor=None

        super(Doctor,self).save()
        doctor=self
        message='دکتر ذخیره شد.'
        result=SUCCEED
        return result,message,doctor
    
    @property
    def last_name(self):
        return self.person_account.person.last_name
    @property
    def first_name(self):
        return self.person_account.person.first_name
    @property
    def image(self):
        return self.person_account.person.image
    
    @property
    def melli_code(self):
        return self.person_account.person.melli_code
    @property
    def father_name(self):
        return self.person_account.person.father_name
   
class Prescription(Invoice): 
    class Meta:
        verbose_name = _("نسخه")
        verbose_name_plural = _("نسخه ها")
 

    def save(self,*args, **kwargs):
        result=FAILED
        message=''
        prescription=None

        if self.class_name is None or self.class_name=="":
            self.class_name="prescription"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(Prescription,self).save()
        prescription=self
        message='نسخه ذخیره شد.'
        result=SUCCEED
        return result,message,prescription
     
class PrescriptionLine(InvoiceLine):

    class Meta:
        verbose_name = _("PrescriptionLine")
        verbose_name_plural = _("PrescriptionLines")
 
 