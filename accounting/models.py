from django.db import models
from .apps import APP_NAME
from django.utils.translation import gettext as _
from utility.qrcode import generate_qrcode
from utility.repo import ParameterRepo
from utility.enums import *
from .constants import *
from utility.constants import FAILED,SUCCEED
from utility.currency import to_price_colored,to_price,CURRENCY
from .enums import *
from utility.calendar import PersianCalendar
from utility.models import LinkHelper,ImageHelper,DateTimeHelper
from tinymce.models import HTMLField
from django.shortcuts import reverse
from django.core.files.storage import FileSystemStorage
from core.models import Event as CoreEvent,Page as CorePage
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
    level=models.IntegerField(_("level"))
    priority=models.IntegerField(_("priority"),default=100)
    bedehkar=models.IntegerField(_("bedehkar"),default=0)
    bestankar=models.IntegerField(_("bestankar"),default=0)
    balance=models.IntegerField("balance",default=0)
    
    
    class_name='account'
    app_name=APP_NAME

    class Meta:
        verbose_name = _("حساب")
        verbose_name_plural = _("حساب ها")

    def __str__(self):
        return f'{self.code}-l{self.level} - {self.type} - {self.name}'
    def get_link(self):
            return f"""
                    <a href="{self.get_absolute_url()}" class="ml-2 text-{self.color}"><span>{self.code}</span> {self.name} <span class="badge badge-{self.color}">{self.type}</span></a>
                    """
     

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
        
        if self.parent is None:
            self.level=0
        else:
            self.level=self.parent.level+1
    
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




class EventCategory(models.Model,LinkHelper):
    class_name="eventcategory"
    app_name=APP_NAME
    title=models.CharField(_("title"), max_length=50)
    color_origin=models.CharField(_("color"),choices=ColorEnum.choices,null=True,blank=True, max_length=50)
    @property
    def color(self):
        if self.color_origin:
            return self.color_origin
        if self.title=="هزینه":
            return "danger"
        return 'primary'
    class Meta:
        verbose_name = 'EventCategory'
        verbose_name_plural = 'EventCategories' 
    def __str__(self):
        return self.title
 

class FinancialEvent(CoreEvent,DateTimeHelper):
    bedehkar=models.ForeignKey("account", related_name="bedehkar_events",verbose_name=_("دریافت کننده"), on_delete=models.PROTECT)
    bestankar=models.ForeignKey("account",related_name="bestankar_events", verbose_name=_("پرداخت کننده"), on_delete=models.PROTECT)
    creator=models.ForeignKey("authentication.profile",null=True,blank=True, verbose_name=_("ثبت شده توسط"), on_delete=models.SET_NULL)
    category=models.ForeignKey("eventcategory",null=True,blank=True, verbose_name=_("دسته بندی"), on_delete=models.SET_NULL)
    tax_percent=models.IntegerField(_("درصد مالیات"),default=-1)
    amount=models.IntegerField(_("مبلغ"),default=0)
    discount=models.IntegerField(_("تخفیف"),default=0)
    payment_method=models.CharField(_("نوع پرداخت"),choices=PaymentMethodEnum.choices,default=PaymentMethodEnum.DRAFT, max_length=50)
      
    @property
    def tax_amount(self):
        return self.amount*self.tax_percent/100
    @property
    def sum_total(self):
        return self.tax_amount+self.amount

    class Meta:
        verbose_name = _("رویداد مالی")
        verbose_name_plural = _("رویداد های مالی")

    def __str__(self):
        return f"{self.title} , {self.bedehkar},  {self.bestankar} , {to_price(self.amount)}"
 
    

    def save(self,*args, **kwargs):
        if self.tax_percent is None or self.tax_percent==-1:
            TAX_PERCENT=ParameterRepo(request=None,app_name=APP_NAME,forced=True).parameter(name="درصد پیش فرض مالیات برای رویدادها",default=10).int_value
            self.tax_percent=TAX_PERCENT
        if self.class_name is None or self.class_name=="":
            self.class_name="financialevent"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(FinancialEvent,self).save()

class InvoiceLineItem(CorePage,LinkHelper):
    class_name="invoicelineitem"
    app_name=APP_NAME
    class Meta:
        verbose_name = _("InvoiceLineItem")
        verbose_name_plural = _("InvoiceLineItems")
 



class InvoiceLineItemUnit(models.Model,LinkHelper,DateTimeHelper):
    invoice_line_item=models.ForeignKey("invoicelineitem", verbose_name=_("invoicelineitem"), on_delete=models.CASCADE)
    unit_name=models.CharField(_("unit_name"),choices=UnitNameEnum.choices, max_length=50)
    coef=models.FloatField(_("coef"),default=1)
    unit_price=models.IntegerField(_("unit_price"),default=1)
    date_added=models.DateTimeField(_("تاریخ "), auto_now=False, auto_now_add=True)

    class_name="invoicelineitemunit"
    app_name=APP_NAME

    class Meta:
        verbose_name = _("InvoiceLineItemUnit")
        verbose_name_plural = _("InvoiceLineItemUnits")

    def __str__(self):
        return f"{self.invoice_line_item}  # هر {self.unit_name}  {to_price(self.unit_price)} {CURRENCY}"
    
class Product(InvoiceLineItem):
    barcode=models.CharField(_("barcode"),null=True,blank=True, max_length=50)
    
    class_name="product"
    app_name=APP_NAME
    def save(self):
        if self.class_name is None or self.class_name=="":
            self.class_name="product"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(Product,self).save()


    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
 
class Service(InvoiceLineItem):

    
    class_name="service"
    app_name=APP_NAME

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
 
    def save(self):
        if self.class_name is None or self.class_name=="":
            self.class_name="service"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(Service,self).save()