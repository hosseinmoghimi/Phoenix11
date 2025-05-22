from django.db import models
from .apps import APP_NAME
from django.utils.translation import gettext as _
from utility.qrcode import generate_qrcode
from utility.enums import *
from .constants import *
from utility.constants import FAILED,SUCCEED
from utility.currency import to_price_colored
from .enums import *
from utility.calendar import PersianCalendar
from utility.models import LinkHelper,ImageHelper,DateTimeHelper
from tinymce.models import HTMLField
from django.shortcuts import reverse
from django.core.files.storage import FileSystemStorage
from phoenix.server_settings import UPLOAD_ROOT,QRCODE_ROOT,QRCODE_URL,STATIC_URL,MEDIA_URL,ADMIN_URL,FULL_SITE_URL
IMAGE_FOLDER = "images/"
from .settings_on_server import  NO_DUPLICATED_ACCOUNT_NAME,NO_DUPLICATED_ACCOUNT_CODE
upload_storage = FileSystemStorage(location=UPLOAD_ROOT, base_url='/uploads')

class Account(models.Model,LinkHelper):
    parent=models.ForeignKey("account", verbose_name=_("parent"),null=True,blank=True, on_delete=models.CASCADE)
    name=models.CharField(_("name"), max_length=50)
    color=models.CharField(_("color"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY, max_length=50)
    code=models.CharField(_("code"), max_length=50)
    type=models.CharField(_("نوع"),choices=AccountTypeEnum.choices, max_length=50)
    nature=models.CharField(_("ماهیت"),choices=AccountNatureEnum.choices,default=AccountNatureEnum.FREE, max_length=50)
    description=models.CharField(_("description"),null=True,blank=True, max_length=500)
    logo_origin=models.ImageField(_("logo"),blank=True,null=True, upload_to=IMAGE_FOLDER+"account", height_field=None, width_field=None, max_length=None)
    priority=models.IntegerField(default=100)
    bedehkar=models.IntegerField(_("bedehkar"),default=0)
    bestankar=models.IntegerField(_("bestankar"),default=0)
    balance=models.IntegerField("balance",default=0)
    
    
    class_name='account'
    app_name=APP_NAME

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")

    def __str__(self):
        return f'{self.code}-l{self.level} - {self.type} - {self.name}'
    def get_link(self):
            return f"""
                    <a href="{self.get_absolute_url()}" class="ml-2 text-{self.color}"><span>{self.code}</span> {self.name} <span class="badge badge-{self.color}">{self.type}</span></a>
                    """
    
    @property
    def level(self):
        if self.parent is None:
            return 0
        return self.parent.level+1

    def childs(self):
        return self.account_set.all()

    def all_childs(self): 
        return Account.objects.filter(pk__in=self.all_sub_accounts_id())
         

    def get_breadcrumb_link(self):
        if self.parent is None:
            return  self.get_link() 
        # return self.parent.get_breadcrumb_link()+f"""<span class="my-2">{ACCOUNT_NAME_SEPERATOR}</span>"""+self.get_link()
        return f"""<div>{self.parent.get_breadcrumb_link()}</div><div>{self.get_link()}</div>"""
        # return f"""<span>{self.parent.get_breadcrumb_link()}</span>{ACCOUNT_NAME_SEPERATOR}<span>{self.get_link()}</span>"""

    def save(self): 
        result=SUCCEED
        message="موفقیت آمیز"
        if NO_DUPLICATED_ACCOUNT_NAME and len(Account.objects.filter(name=self.name).exclude(pk=self.pk))>0:
            result=FAILED
            message="نام تکراری"
        if NO_DUPLICATED_ACCOUNT_CODE and len(Account.objects.filter(code=self.code).exclude(pk=self.pk))>0:
            result=FAILED
            message="کد تکراری"
        if result==FAILED:
            return result,message,self 
        global ACCOUNT_LEVEL_NAMES
        from .settings_on_server import ACCOUNT_LEVEL_NAMES 
        self.type=AccountTypeEnum.GROUP
        self.type=ACCOUNT_LEVEL_NAMES[self.level]
        result=FAILED
        if NO_DUPLICATED_ACCOUNT_CODE:
            dup=Account.objects.filter(code=self.code).exclude(pk=self.pk).first()
            if dup is not None:
                message="کد حساب تکراری است."
                result=FAILED
                return result,message,None
        if NO_DUPLICATED_ACCOUNT_NAME:
            dup=Account.objects.filter(name=self.name).exclude(pk=self.pk).first()
            if dup is not None:
                message="نام حساب تکراری است."
                result=FAILED
                return result,message,None
        if self.color is None and self.parent is not None:
            self.color=self.parent.color
        super(Account,self).save()
        result=SUCCEED
        message="با موفقیت اضافه گردید."
        return result,message,self
 
  
    
    def all_sub_accounts_lines(self):
        ids=self.all_sub_accounts_id()
        return AccountingDocumentLine.objects.filter(account_id__in=ids)

    def all_sub_accounts_id(self):
        ids=[self.id]
        for child in self.childs:
            for id in child.all_sub_accounts_id():
                ids.append(id)
        return ids

    @property
    def person(self):
        pa= PersonAccount.objects.filter(pk=self.pk).first()
        if pa is not None:
            return pa.person
        
        

    def normalize_total(self):
        # print(self.full_title)
        bedehkar=0
        bestankar=0
        balance=0
        for accounting_document_line in AccountingDocumentLine.objects.filter(account_id=self.pk): 
            # basic_account.normalize_total()
            bedehkar+=accounting_document_line.bedehkar
            bestankar+=accounting_document_line.bestankar
        childs=self.childs
        if len(childs)>0:
            for acc in childs:
                bedehkar+=acc.bedehkar
                bestankar+=acc.bestankar
        balance=bestankar-bedehkar
        self.bedehkar=bedehkar
        self.bestankar=bestankar
        self.balance=balance
        self.save() 
        if self.parent is not None:
            self.parent.normalize_total()
    @property
    def logo(self):
        if not self.logo_origin :
            return f"{STATIC_URL}{APP_NAME}/img/pages/thumbnail/account.png"
        return f"{MEDIA_URL}{self.logo_origin}"
   #test
    @property
    def balance_colored(self):
        return to_price_colored(self.balance)
 

    @property
    def childs(self):
   
       
        childs=Account.objects.filter(parent_id=self.pk)
        return childs

    @property  
    def full_name(self):
        if self.parent is None:
            return self.name
        return self.parent.full_name+ACCOUNT_NAME_SEPERATOR+self.name

