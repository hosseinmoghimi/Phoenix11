from .models import OrganizationUnit,Employee 
from .apps import APP_NAME
from .enums import *
from log.repo import LogRepo 
from django.db.models import Q
from django.shortcuts import reverse
from authentication.repo import ProfileRepo
from accounting.repo import InvoiceLineItemUnitRepo
from utility.num import filter_number
from utility.calendar import PersianCalendar
from utility.constants import FAILED,SUCCEED
from utility.log import leolog
from .enums import *
 


class OrganizationUnitRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=OrganizationUnit.objects.filter(id=0)
        profile=ProfileRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=OrganizationUnit.objects
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
        
    def organization_unit(self,*args, **kwargs):
        if "organization_unit_id" in kwargs and kwargs["organization_unit_id"] is not None:
            return self.objects.filter(pk=kwargs['organization_unit_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_organization_unit(self,*args,**kwargs):
        result,message,organization_unit=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_organizationunit"):
            message="دسترسی غیر مجاز"
            return result,message,organization_unit
        organization_unit=OrganizationUnit()
        if 'name' in kwargs:
            organization_unit.name=kwargs["name"]
        if 'parent_id' in kwargs :
            if kwargs["parent_id"] is not None and kwargs["parent_id"]>0:
                organization_unit.parent_id=kwargs["parent_id"]
        if 'account_id' in kwargs:
            organization_unit.my_account_id=kwargs["account_id"]
            # from accounting.models import Account
            # account=Account.objects.filter(id=kwargs['account_id']).first()
            # if account is not None:
            #     organization_unit.account_code=account.code
          

        if 'title' in kwargs:
            organization_unit.title=kwargs["title"]
        
        (result,message,organization_unit)=organization_unit.save()
        return result,message,organization_unit

 

class EmployeeRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Employee.objects.filter(id=0)
        profile=ProfileRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=Employee.objects
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
        
    def employee(self,*args, **kwargs):
        if "employee_id" in kwargs and kwargs["employee_id"] is not None:
            return self.objects.filter(pk=kwargs['employee_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_employee(self,*args,**kwargs):
        result,message,employee=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_organizationunit"):
            message="دسترسی غیر مجاز"
            return result,message,employee
        employee=Employee()
        if 'job_title' in kwargs:
            employee.job_title=kwargs["job_title"]
        if 'person_id' in kwargs:
            if kwargs["person_id"]>0:
                employee.person_id=kwargs["person_id"]
        if 'organization_unit_id' in kwargs:
            if kwargs["organization_unit_id"]>0:
                employee.organization_unit_id=kwargs["organization_unit_id"]
         


        if 'title' in kwargs:
            employee.title=kwargs["title"]
        
        (result,message,employee)=employee.save()
        return result,message,employee

 