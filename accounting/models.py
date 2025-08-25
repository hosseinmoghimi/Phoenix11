from django.db import models
from django.db.models import Q
from .apps import APP_NAME
from django.utils.translation import gettext as _
from utility.qrcode import generate_qrcode
from utility.repo import ParameterRepo
from utility.enums import *
from .constants import *
from utility.utils import fixed_length
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
from .settings_on_server import  NO_DUPLICATED_ACCOUNT_NAME,NO_DUPLICATED_ACCOUNT_CODE
from django.utils import timezone
from utility.log import leolog
upload_storage = FileSystemStorage(location=UPLOAD_ROOT, base_url='/uploads')
IMAGE_FOLDER = "images/"
try:
    from accounting.settings_on_server import DELETE_OLD_ITEM_UNIT
except:
    DELETE_OLD_ITEM_UNIT=True

class PersonAccountHelper:

    @property
    def economic_no(self):
        economic_no=''
        person_account=PersonAccount.objects.filter(pk=self.pk).first()
        if person_account is not None:
            economic_no=person_account.person.economic_no
        return economic_no
    
    @property
    def person(self):
        pa= PersonAccount.objects.filter(pk=self.pk).first()
        if pa is not None:
            return pa.person
        
    
    @property
    def melli_id(self):
        return self.melli_code
    
    @property 
    def thumbnail(self):
         
        thumbnail=""
        if self.thumbnail_origin is None or str(self.thumbnail_origin)=="":
            try:
                person_account=PersonAccount.objects.filter(pk=self.pk).first()
                if person_account is not None:
                    person=person_account.person
                    if person.image_origin is None or str(person.image_origin)=="":
                        return person.image
            except:
                pass
        else:
            thumbnail= f"{MEDIA_URL}{self.thumbnail_origin}"

        return thumbnail
    @property
    def melli_code(self):
        melli_code=''
        person_account=PersonAccount.objects.filter(pk=self.pk).first()
        if person_account is not None:
            melli_code=person_account.person.melli_code
        return melli_code
    

    
    @property
    def tel(self):
        tel=''
        person_account=PersonAccount.objects.filter(pk=self.pk).first()
        if person_account is not None:
            tel=person_account.person.tel
        return tel
    
    @property
    def postal_code(self):
        postal_code=''
        person_account=PersonAccount.objects.filter(pk=self.pk).first()
        if person_account is not None:
            postal_code=person_account.person.postal_code
        return postal_code
    

    @property
    def address(self):
        address=''
        person_account=PersonAccount.objects.filter(pk=self.pk).first()
        if person_account is not None:
            address=person_account.person.address
        return address
    

class Account(CorePage,LinkHelper,PersonAccountHelper):
    code=models.CharField(_("code"),null=True,blank=True, max_length=50)
    type=models.CharField(_("نوع"),choices=AccountTypeEnum.choices, max_length=50)
    nature=models.CharField(_("ماهیت"),choices=AccountNatureEnum.choices,default=AccountNatureEnum.FREE, max_length=50)
    level=models.IntegerField(_("level"))
    bedehkar=models.IntegerField(_("bedehkar"),default=0)
    bestankar=models.IntegerField(_("bestankar"),default=0)
    balance=models.IntegerField("balance",default=0)
    
 
    def balance_color(self):
        if self.balance==0:
            return 'primary'
        if self.balance>0:
            return 'success'
        if self.balance<0:
            return 'danger'
 
     
    
    @property
    def name(self):
        return self.title    
    
    class_name='account'
    app_name=APP_NAME

    class Meta:
        verbose_name = _("حساب")
        verbose_name_plural = _("حساب ها")

    def __str__(self):
        return f'{self.code}-level {self.level} - {self.type} - {self.title}'
    def get_link(self):
            return f"""
                    <a href="{self.get_absolute_url()}" class="ml-2 text-{self.color}"><span>{self.code}</span> {self.title} <span class="badge badge-{self.color}">{self.type}</span></a>
                    """
     

    def childs(self):
        return self.account_set.all()

    def all_childs(self): 
        return Account.objects.filter(pk__in=self.all_sub_accounts_id())
         
    @property
    def parent_account(self):
        if self.parent is not None:
            return Account.objects.filter(id=self.parent.id).first()
        return None
    def get_breadcrumb_link(self):
        if self.parent is None:
            return  self.get_link() 
        # return self.parent.get_breadcrumb_link()+f"""<span class="my-2">{ACCOUNT_NAME_SEPERATOR}</span>"""+self.get_link()
        
        return f"""<div>{self.parent_account.get_breadcrumb_link()}</div><div>{self.get_link()}</div>"""
        # return f"""<span>{self.parent.get_breadcrumb_link()}</span>{ACCOUNT_NAME_SEPERATOR}<span>{self.get_link()}</span>"""

    def save(self,*args, **kwargs): 

        if self.app_name is None or self.app_name=='':
            self.app_name=APP_NAME
        if self.class_name is None or self.class_name=='':
            self.class_name='account'
        if self.parent is None:
            self.level=0
        else:
            self.level=self.parent_account.level+1

        result=FAILED
        message="خطا"
        
        global ACCOUNT_LEVEL_NAMES
        from .settings_on_server import ACCOUNT_LEVEL_NAMES 
        self.type=AccountTypeEnum.GROUP
        self.type=ACCOUNT_LEVEL_NAMES[self.level]
        result=FAILED
        if NO_DUPLICATED_ACCOUNT_CODE:
            dup=Account.objects.filter(code=self.code).exclude(pk=self.pk).first()
            if dup is not None:
                message="کد حساب تکراری است."
                return FAILED,message,None
        if NO_DUPLICATED_ACCOUNT_NAME:
            dup=Account.objects.filter(title=self.title).exclude(pk=self.pk).first()
            if dup is not None:
                message="نام حساب تکراری است."
                return FAILED,message,None
        if self.color is None and self.parent is not None:
            self.color=self.parent.color

        super(Account,self).save(*args, **kwargs)
       
        account=self
        if self.id is not None:
            result=SUCCEED
            message="حساب با موفقیت اضافه گردید."
        return result,message,account
 
  
    
    def all_sub_accounts_lines(self):
        ids=self.all_sub_accounts_id()
        return FinancialDocumentLine.objects.filter(account_id__in=ids)

    def all_sub_accounts_id(self):
        ids=[self.id]
        for child in self.childs:
            for id in child.all_sub_accounts_id():
                ids.append(id)
        return ids

        

    def normalize(self):
        # print(self.full_title)
        bedehkar=0
        bestankar=0
        balance=0
        for financial_document_line in FinancialDocumentLine.objects.filter(account_id=self.pk): 
            # basic_account.normalize()
            bedehkar+=financial_document_line.bedehkar
            bestankar+=financial_document_line.bestankar
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
            parent=Account.objects.filter(id=self.parent.id).first()
            if parent is not None:
                parent.normalize()
     
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
            return self.title
        return self.parent_account.full_name+ACCOUNT_NAME_SEPERATOR+self.title
 
    
class PersonAccount(Account,LinkHelper):
    person=models.ForeignKey("authentication.person", verbose_name=_("person"), on_delete=models.PROTECT)
    person_category=models.ForeignKey("personcategory", verbose_name=_("person_category"), on_delete=models.PROTECT)
    
    
    @property
    def thumbnail(self):
        if self.thumbnail_origin is not None and not self.thumbnail_origin=='':
            return f"{MEDIA_URL}{self.thumbnail_origin}"
         
        if self.thumbnail_origin is None or str(self.thumbnail_origin)=="":
            if self.person.image_origin is not None and not self.person.image_origin=='':
                return self.person.image
            try:
                return f"{STATIC_URL}{self.app_name}/img/pages/thumbnail/{self.class_name}.png/"
            except:
                pass 


    class_name='personaccount'
    app_name=APP_NAME

    @property
    def category(self):
        return self.person_category.title    

 
        
    class Meta:
        verbose_name = _("PersonAccount")
        verbose_name_plural = _("حساب های اشخاص")

    def __str__(self):
        return self.name
    def generate_code(self,*args, **kwargs):
        code='00' 
        is_available=True
        counter=0
        while is_available:
            counter+=1
            code=fixed_length(self.person_category.code_length,str(counter))
            acc=Account.objects.filter(code=self.person_category.account.code+code).first()
            if acc is None:
                is_available=False
        return self.person_category.account.code+code
    def save(self,*args, **kwargs):
        
        result,message,person_account=FAILED,"",None
        p_a=PersonAccount.objects.filter(person_id=self.person_id).filter(person_category_id=self.person_category_id).first()
        if p_a is not None and self.id is None:
            message="از قبل برای این دسته بندی و شخص حساب مرتبط ایجاد شده است. "
            return result,message,person_account

        person_category=PersonCategory.objects.filter(id=self.person_category_id).first()
        if person_category is not None:
            self.parent=person_category.account
        if self.code is None or self.code==0 or self.code=='':
            self.code=self.generate_code()
        
        self.title=f'{self.person} # {self.category}'
        
        if self.app_name is None or self.app_name=='':
            self.app_name=APP_NAME
        if self.class_name is None or self.class_name=='':
            self.class_name='personaccount'
        result,message,account=super(PersonAccount,self).save(*args, **kwargs)
    
        if self.id is not None:
            result=SUCCEED
            message="حساب شخص با موفقیت ذخیره شد."
            person_account=self
        return result,message,person_account


class FinancialDocument(models.Model,LinkHelper):
    financial_year=models.ForeignKey("financialyear" , verbose_name=_("سال مالی"), on_delete=models.PROTECT)
    title=models.CharField(_("title"), max_length=500)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    date_time=models.DateTimeField(_("date_time"), auto_now=True, auto_now_add=False)
    date_modified=models.DateTimeField(_("date_modified "), auto_now=True, auto_now_add=False)
    status=models.CharField(_("status"),max_length=20,choices=FinancialDocumentStatusEnum.choices,default=FinancialDocumentStatusEnum.DRAFT)
    bedehkar=models.IntegerField(_("بدهکار"),default=0)
    bestankar=models.IntegerField(_("بستانکار"),default=0)
    balance=models.IntegerField(_("تراز"),default=0)
     
    @property 
    def lines(self):
        return self.financialdocumentline_set.all()


    @property 
    def status_color(self):
        if self.status==FinancialDocumentStatusEnum.ACCEPTED:
            return "success"
        if self.status==FinancialDocumentStatusEnum.DENIED:
            return "danger"
        if self.status==FinancialDocumentStatusEnum.DRAFT:
            return "secondary"
        return "primary"

    def save(self):
        if self.financial_year is None:
            self.financial_year=FinancialYear.objects.filter(in_progress=True).first()
        # result,message,financial_document=FAILED,"",self
        # if self.financial_year.start_date>self.date_time or self.financial_year.end_date<self.date_time:
        #     message="تاریخ سند خارج از محدوده تاریخ سال مالی جاری است."
        super(FinancialDocument,self).save()
        result=SUCCEED
        message="با موفقیت اضافه شد."
        return result,message,self

    class_name="financialdocument"
    app_name=APP_NAME    
    class Meta:
        verbose_name = _("سند مالی")
        verbose_name_plural = _("سند های مالی")

    def __str__(self):
        return self.title
 
    def normalize(self):
        bedehkar=0
        bestankar=0
        for line in self.lines:
            bedehkar+=line.bedehkar
            bestankar+=line.bestankar

        self.bedehkar=bedehkar
        self.bestankar=bestankar
        self.balance=bestankar-bedehkar
        self.save()


class Brand(models.Model,LinkHelper,ImageHelper):
    name=models.CharField(_("name"),max_length=100)
    logo_origin=models.ImageField(_("logo"),blank=True,null=True, upload_to=IMAGE_FOLDER+"account", height_field=None, width_field=None, max_length=None)
    class_name="brand"
    app_name=APP_NAME
 
    class Meta:
        verbose_name = _("برند")
        verbose_name_plural = _("برند ها")

    def __str__(self):
        return self.name


class FinancialDocumentLine(models.Model,LinkHelper):
    financial_document=models.ForeignKey("financialdocument", verbose_name=_("accountingdocument"), on_delete=models.CASCADE)
    account=models.ForeignKey("account", verbose_name=_("account"), on_delete=models.PROTECT)
    financial_event=models.ForeignKey("financialevent", null=True,blank=True,verbose_name=_("event"), on_delete=models.PROTECT)
    title=models.CharField(_("title"), max_length=500)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    date_time=models.DateTimeField(_("date_time"), auto_now=False, auto_now_add=False)
    date_modified=models.DateTimeField(_("date_modified "),null=True, auto_now=True, auto_now_add=False)
    bedehkar=models.IntegerField(_("بدهکار"),default=0)
    bestankar=models.IntegerField(_("بستانکار"),default=0)
    balance=models.IntegerField(_("بالانس"),default=0)
    @property
    def amount(self):
        return self.bestankar+self.bedehkar
    @property
    def persian_date_time(self):
        a= PersianCalendar().from_gregorian(self.date_time)    
        return f"""
                    <span>{a[:11]}</span>
                    <small class="text-muted mr-1">{a[11:]}</small>

                """
    def delete(self,*args, **kwargs): 
        account=self.account
        financial_document=self.financial_document
        super().delete(*args, **kwargs)
        financial_document.normalize()
        account.normalize()

    def save(self):

        
        result,message,financial_document_line=FAILED,"",self
        # import datetime
        # import pytz
        # utc=pytz.UTC
        # start_date=utc.localize(self.financial_document.financial_year.start_date)
        # end_date=utc.localize(self.financial_document.financial_year.end_date)
        # date_time=utc.localize(self.date_time)
        # leolog(start_date=start_date,end_date=end_date,date_time=date_time)
        # if self.financial_document.financial_year.start_date>self.date_time or self.financial_document.financial_year.end_date<self.date_time:
        #     message="تاریخ سند خارج از محدوده تاریخ سال مالی جاری است."
        #     return result,message,financial_document

        if not self.bedehkar==0 and not self.bestankar==0:
            message='مبلغ بدهکار و بستانکار صفر وارد شده است.'
            return result,message,None
        if self.account.nature==AccountNatureEnum.ONLY_BEDEHKAR and self.bestankar>0:
            message='ماهیت حساب فقط بدهکار است.'
            return result,message,None
        if self.account.nature==AccountNatureEnum.ONLY_BESTANKAR and self.bedehkar>0:
            message='ماهیت حساب فقط بستانکار است.'
            return result,message,None
        
        if self.financial_event_id ==0:
            message='رویداد مالی انتخاب نشده است.'
            return result,message,None
        if self.financial_document_id is None or self.financial_document_id==0:
            message='سند مالی انتخاب نشده است.'
            return result,message,None
        super(FinancialDocumentLine,self).save()
        self.financial_document.normalize()
        self.account.normalize()
        result=SUCCEED
        message='سطر سند مالی با موفقیت اضافه شد.'
        return result,message,financial_document_line
    @property
    def rest(self):
        return 0
    @property
    def amount(self):  
        return self.bedehkar+self.bestankar
    class_name="financialdocumentline"
    app_name=APP_NAME 

    class Meta:
        verbose_name = _("سطر سند حسابداری")
        verbose_name_plural = _("سطر های سند حسابداری")

    def __str__(self):
        event=""
        if self.financial_event is not None :
            event=self.financial_event.title
        return f"{self.account.id} , {event} , {self.account.name} , {to_price(self.balance)}, {to_price(self.bestankar)}, {to_price(self.bedehkar)}"


class FinancialYear(models.Model,LinkHelper,DateTimeHelper):
    name=models.CharField(_("نام"),max_length=50)
    start_date=models.DateTimeField(_("تاریخ شروع"), auto_now=False, auto_now_add=False)
    end_date=models.DateTimeField(_("تاریخ پایان"), auto_now=False, auto_now_add=False)
    description=models.CharField(_("description"),max_length=20,null=True,blank=True)
    status=models.CharField(_("status"),max_length=20,choices=FinancialYearStatusEnum.choices,default=FinancialYearStatusEnum.SUSPEND)
    in_progress=models.BooleanField(_("in progress"),default=False)
    class_name='financialyear'
    app_name=APP_NAME

    class Meta:
        verbose_name = _("سال مالی")
        verbose_name_plural = _("سال های مالی")
    def __str__(self):
        return self.name+' #' if self.in_progress else ''

    def save(self):
        result,message,financial_year=FAILED,"",self
        result=SUCCEED
        message=""
        if self.in_progress or self.status==FinancialYearStatusEnum.IN_PROGRESS:
            self.in_progress=True
            self.status=FinancialYearStatusEnum.IN_PROGRESS
            for f_y in FinancialYear.objects.exclude(pk=self.pk):
                f_y.status=FinancialYearStatusEnum.SUSPEND
                f_y.in_progress=False
                super(FinancialYear,f_y).save()
        else:
            self.in_progress=False

        super(FinancialYear,self).save()
        return result,message,financial_year


class PersonCategory(models.Model,LinkHelper):
    title=models.CharField(_("title"),choices=PersonCategoryEnum.choices,default=PersonCategoryEnum.DEFAULT, max_length=50)
    account=models.ForeignKey("account", verbose_name=_("account"), on_delete=models.PROTECT)
    code_length=models.IntegerField(_("code_length"),default=5)
   
    class_name="personcategory"
    app_name=APP_NAME

    @property
    def count_of_accounts(self):
        return len(self.personaccount_set.all())
    
    @property
    def count(self):
        return len(PersonAccount.objects.filter(category=self.category))
        
    @property
    def persons(self):
        person_accounts=PersonAccount.objects.filter(person_category=self)
        person_ids=[]
        for p_a in person_accounts:
            person_ids.append(p_a.person_id)
        return Person.objects.filter(pk__in=person_ids)
    class Meta:
        verbose_name = _("دسته بندی اشخاص")
        verbose_name_plural = _("دسته بندی های اشخاص")

    def __str__(self):
        return self.title


class FinancialEvent(CoreEvent,DateTimeHelper):
    bedehkar=models.ForeignKey("account", related_name="bedehkar_events",verbose_name=_("دریافت کننده"), on_delete=models.PROTECT)
    bestankar=models.ForeignKey("account",related_name="bestankar_events", verbose_name=_("پرداخت کننده"), on_delete=models.PROTECT)
    creator=models.ForeignKey("authentication.person",null=True,blank=True, verbose_name=_("ثبت شده توسط"), on_delete=models.SET_NULL)
    tax_percentage=models.IntegerField(_("درصد مالیات"),default=0)
    amount=models.IntegerField(_("مبلغ"),default=0)
    discount=models.IntegerField(_("تخفیف"),default=0)
    payment_method=models.CharField(_("نوع پرداخت"),choices=PaymentMethodEnum.choices,default=PaymentMethodEnum.DRAFT, max_length=50)
    shipping_fee=models.IntegerField(_("هزینه حمل"),default=0)
    # status=models.CharField(_("status"),choices=FinancialEventStatusEnum.choices,default=FinancialEventStatusEnum.DRAFT, max_length=50)

    @property
    def tax_amount(self):
        return self.amount*self.tax_percentage/100
    @property
    def sum_total(self):
        return self.tax_amount+self.amount-self.discount

    class Meta:
        verbose_name = _("رویداد مالی")
        verbose_name_plural = _("رویداد های مالی")

    def __str__(self):
        return f"{self.title} , {self.bedehkar},  {self.bestankar} , {to_price(self.amount)} {CURRENCY}"
 
    

    def save(self,*args, **kwargs):
        result,message,financial_event=FAILED,'',self
        if self.tax_percentage is None or self.tax_percentage==-1:
            TAX_PERCENT=ParameterRepo(request=None,app_name=APP_NAME,forced=True).parameter(name="درصد پیش فرض مالیات برای رویدادها",default=10).int_value
            self.tax_percent=TAX_PERCENT
        if self.class_name is None or self.class_name=="":
            self.class_name="financialevent"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        result=SUCCEED
        message='رویداد مالی با موفقیت اضافه شد.'
        super(FinancialEvent,self).save()
        return result,message,financial_event
 

class InvoiceLineItem(CorePage,LinkHelper):
    class_name="invoicelineitem"
    app_name=APP_NAME
    class Meta:
        verbose_name = _("InvoiceLineItem")
        verbose_name_plural = _("موارد قابل فروش")

    @property    
    def unit_name(self):
        unit= InvoiceLineItemUnit.objects.filter(invoice_line_item_id=self.id).filter(default=True).first()
        if unit is not None:
            return unit.unit_name
        return UnitNameEnum.ADAD
    @property    
    def unit_price(self):
        unit= InvoiceLineItemUnit.objects.filter(invoice_line_item_id=self.id).filter(default=True).first()
        if unit is not None:
            return unit.unit_price
        return 0


class InvoiceLineItemUnit(models.Model,LinkHelper,DateTimeHelper):
    invoice_line_item=models.ForeignKey("invoicelineitem",related_name="units" ,verbose_name=_("invoicelineitem"), on_delete=models.CASCADE)
    unit_name=models.CharField(_("unit_name"),choices=UnitNameEnum.choices, max_length=50)
    coef=models.FloatField(_("coef"),default=1)
    unit_price=models.IntegerField(_("unit_price"),default=1)
    date_added=models.DateTimeField(_("تاریخ "), auto_now=False, auto_now_add=True)
    default=models.BooleanField(_("default"),default=False)
    class_name="invoicelineitemunit"
    app_name=APP_NAME

    @property
    def percentage_tag(self):
        base=InvoiceLineItemUnit.objects.filter(invoice_line_item_id=self.invoice_line_item_id).filter(coef=1).first()
        if base is not None:
            base_price=base.unit_price
            if base_price==0:
                return ""
            color='primary'
            perc=(base_price-(self.unit_price/self.coef))/base_price*100
            perc=int(perc)
            if base_price>(self.unit_price/self.coef):
                color='success'

            if base_price<(self.unit_price/self.coef):
                color='danger'
                perc=0-perc
            if perc==0:
                return ""
            return f"""<span class='text-{color}'>{perc} %</span>"""
        return ""
    class Meta:
        verbose_name = _("InvoiceLineItemUnit")
        verbose_name_plural = _("واحد های قابل فروش")
    @property
    def product(self):
        return Product.objects.filter(pk=self.invoice_line_item_id).first()
    
    def __str__(self):
        return f"{self.invoice_line_item}  # هر {self.unit_name}  {to_price(self.unit_price)} {CURRENCY} #  {str(self.default)} "
    
    def save(self):
        invoice_line_item_units=InvoiceLineItemUnit.objects.filter(invoice_line_item_id=self.invoice_line_item.id)
        invoice_line_item_units_with_this_unit=invoice_line_item_units.filter(unit_name=self.unit_name)
        for invoice_line_item_unit in invoice_line_item_units_with_this_unit:
            if invoice_line_item_unit.unit_price==0:
                invoice_line_item_unit.delete()
            else:
                if self.default is True:
                    invoice_line_item_unit.default=False
                    super(InvoiceLineItemUnit,invoice_line_item_unit).save()
        if DELETE_OLD_ITEM_UNIT:
            invoice_line_item_units_with_this_unit.delete()
        # Now=timezone.now()
        # self.date_added=Now
        if self.default is True:
            other_invoice_line_item_units=invoice_line_item_units.filter(default=True)
            for other_invoice_line_item_unit in other_invoice_line_item_units:
                other_invoice_line_item_unit.default=False
                other_invoice_line_item_unit.save()

        super(InvoiceLineItemUnit,self).save()


class Category(models.Model,LinkHelper,ImageHelper):
    class_name="category"
    app_name=APP_NAME
    
    parent=models.ForeignKey("category", verbose_name=_("parent"),null=True,blank=True, on_delete=models.SET_NULL)
    title=models.CharField(_("title"),max_length=100)
    priority=models.IntegerField(_("priority"),default=100)
    thumbnail_origin = models.ImageField(_("تصویر کوچک"), upload_to=IMAGE_FOLDER+'ImageBase/Thumbnail/',null=True, blank=True, height_field=None, width_field=None, max_length=None)
    header_origin = models.ImageField(_("تصویر سربرگ"), upload_to=IMAGE_FOLDER+'ImageBase/Header/',null=True, blank=True, height_field=None, width_field=None, max_length=None)
    products=models.ManyToManyField("product",blank=True, verbose_name=_("products"))
    def get_link(self):
            return f"""
                    <a href="{self.get_absolute_url()}" class="ml-2 "> {self.title} </a>
                    """
    def get_market_link(self):
            return f"""
                    <a href="{self.get_market_absolute_url()}" class="ml-2 "> {self.title} </a>
                    """
    
    def all_childs_products(self):
        ids=self.childs_ids()
        p_ids=[]
        for category in Category.objects.filter(Q(id__in=ids) | Q(id=self.pk)):
            for product in category.products.all():
                p_ids.append(product.id)
        return Product.objects.filter(id__in=p_ids)

    def childs_ids(self):
        ids=[]
        childs=Category.objects.filter(parent_id=self.pk)
        if len(childs)==0:
            return []
        for child in childs:
            ids2=child.childs_ids()
            for id in ids2:
                ids.append(id)
        return ids
    class Meta:
        verbose_name = _("دسته بندی")
        verbose_name_plural = _("دسته بندی ها")

    def __str__(self):
        return self.title

    def get_market_absolute_url(self):
        return reverse("market:category",kwargs={'pk':self.pk})
        
    def get_breadcrumb_link(self):
        if self.parent is None:
            return  self.get_link() 
        # return self.parent.get_breadcrumb_link()+f"""<span class="my-2">{ACCOUNT_NAME_SEPERATOR}</span>"""+self.get_link()
        return f""" {self.parent.get_breadcrumb_link()} / {self.get_link()} """
        # return f"""<span>{self.parent.get_breadcrumb_link()}</span>{ACCOUNT_NAME_SEPERATOR}<span>{self.get_link()}</span>"""
    def get_market_breadcrumb_link(self):
        if self.parent is None:
            return  self.get_market_link() 
        # return self.parent.get_breadcrumb_link()+f"""<span class="my-2">{ACCOUNT_NAME_SEPERATOR}</span>"""+self.get_link()
        return f""" {self.parent.get_market_breadcrumb_link()} / {self.get_market_link()} """
        # return f"""<span>{self.parent.get_breadcrumb_link()}</span>{ACCOUNT_NAME_SEPERATOR}<span>{self.get_link()}</span>"""
    @property
    def full_title(self):
        if self.parent is None:
            return self.title
        return self.parent.full_title+" / "+self.title

    def save(self):
        result,message,category=FAILED,'',self
        super(Category,self).save()
        result=SUCCEED
        message='دسته بندی با موفقیت اضافه شد.'
        return result,message,category


class Product(InvoiceLineItem):
    brand=models.ForeignKey("brand",null=True,blank=True, verbose_name=_("brand"), on_delete=models.CASCADE)
    model=models.CharField(_("model"),null=True,blank=True, max_length=50)
    barcode=models.CharField(_("barcode"),null=True,blank=True, max_length=50)
    
    class_name="product"
    app_name=APP_NAME
    def save(self):
        result,message,product=FAILED,"",None
        if self.class_name is None or self.class_name=="":
            self.class_name="product"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        
        super(Product,self).save()
        result=SUCCEED
        product=self
        message="کالای جدید افزوده شد."
        return result,message,product


    class Meta:
        verbose_name = _("کالا")
        verbose_name_plural = _("کالا ها")
 
    def get_market_absolute_url(self):
        return reverse("market:product",kwargs={'pk':self.pk})
    
  
class ProductSpecification(models.Model,LinkHelper):
    product=models.ForeignKey("product", verbose_name=_("product"), on_delete=models.CASCADE)
    name=models.CharField(_("name"),max_length=50)
    value=models.CharField(_("value"),max_length=50)

    class_name="productspecification"
    app_name=APP_NAME
    class Meta:
        verbose_name = _("ProductSpecification")
        verbose_name_plural = _("ویژگی های محصولات")

    def __str__(self):
        return f"{self.product} > {self.name} > {self.value}"


class Service(InvoiceLineItem):

    
    class_name="service"
    app_name=APP_NAME

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("خدمات")
 
    def save(self):
        (result,message,service)=FAILED,'',self
        if self.class_name is None or self.class_name=="":
            self.class_name="service"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(Service,self).save()
        result=SUCCEED
        message='سرویس جدید با موفقیت اضافه شد.'
        return (result,message,service)


class Invoice(FinancialEvent):
    
    @property
    def lines(self):
        return InvoiceLine.objects.filter(invoice_id=self.id).order_by('row')
    @property
    def line_discount_amount(self):
        line_discount_amount=0
        for line in self.invoiceline_set.all():
            line_discount_amount+=line.discount_percentage*line.unit_price*line.quantity/100
        return line_discount_amount
    class Meta:
        verbose_name = _("فاکتور")
        verbose_name_plural = _("فاکتور ها")

    def get_print_url(self):
        return reverse(APP_NAME+':invoice_print',kwargs={'pk':self.pk})
    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name="invoice"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME

        result,message,invoice=FAILED,"",self
        result=SUCCEED
        message='فاکتور با موفقیت اضافه شد.'
        self.normalize()
         
        return result,message,invoice


    def normalize(self): 
        
        total=0
        discount=0
        tax=0
        amount=0
        shipping_fee=self.shipping_fee
        i=1
        for line in self.invoiceline_set.order_by('row'):
            total+=line.unit_price*line.quantity 
            discount+=line.discount
            line.row=i
            i+=1
            # super(InvoiceLine,line).save()

        total_after_discount=total-discount
        tax=(total_after_discount)*(self.tax_percentage)/100
        amount=total-discount+tax+shipping_fee
        self.amount=amount
        super(Invoice,self).save()
        try:
            for project in self.project_set.all():
                project.normalize()
                pass
        except:
            pass

    @property
    def statistics(self):
        total=0
        discount=0
        tax=0
        amount=0
        shipping_fee=0
        for line in self.invoiceline_set.all():
            total+=line.unit_price*line.quantity 
            discount+=line.discount
        total_after_discount=total-discount
        tax=(total_after_discount)*(self.tax_percentage)/100
        amount=total-discount+tax+shipping_fee
        return (total,discount,total_after_discount,tax,amount)
    
    def get_edit_view_url(self):
        return reverse(APP_NAME+':invoice_edit',kwargs={'pk':self.pk})
    

class InvoiceLine(models.Model,LinkHelper):
    invoice=models.ForeignKey("invoice", verbose_name=_("invoice"), on_delete=models.PROTECT)
    invoice_line_item=models.ForeignKey("invoicelineitem", verbose_name=_("invoice_line_item"), on_delete=models.PROTECT)
    row=models.IntegerField(_("row"),default=0)
    quantity=models.FloatField(_("quantity"))
    unit_name=models.CharField(_("unit_name"),choices=UnitNameEnum.choices, max_length=50)
    unit_price=models.IntegerField(_("unit_price"))
    discount_percentage=models.IntegerField(_("discount_percentage"),default=0)
    tax_amount=models.IntegerField(_("tax_amount"),default=0)
    description=models.CharField(_("description"),null=True,blank=True, max_length=5000)

    class_name="invoiceline"
    app_name=APP_NAME
    class Meta:
        verbose_name = _("InvoiceLine")
        verbose_name_plural = _("سطر های فاکتور ها")
    @property
    def discount(self):
        return self.discount_percentage*self.unit_price*self.quantity/100
    

    def delete(self,*args, **kwargs):
        invoice=self.invoice
        super(InvoiceLine,self).delete()
        self.invoice.normalize()



    @property
    def line_total(self):
        return (100-self.discount_percentage)*self.unit_price*self.quantity/100

    def save(self,*args, **kwargs):

        super(InvoiceLine,self).save()
        result,message=FAILED,''
        self.invoice.normalize()
        if self.id is not None and self.id>0:
            result=SUCCEED
            message='سطر فاکتور با موفقیت اضافه شد.'
        return result,message,self
    def __str__(self):
        return f'{self.invoice}>{self.invoice_line_item}*{self.quantity}'


class Bank(models.Model,LinkHelper):
    name=models.CharField(_("name"),max_length=50)
    branch=models.CharField(_("branch"),null=True,blank=True,max_length=50)
    tel=models.CharField(_("tel"),null=True,blank=True,max_length=50)
    address=models.CharField(_("address"),null=True,blank=True,max_length=50)
    class_name="bank"
    app_name=APP_NAME 

    class Meta:
        verbose_name = _("بانک")
        verbose_name_plural = _("بانک ها")

    def __str__(self):
        return self.name
        
    def save(self): 
        super(Bank,self).save()


class BankAccount(Account):
    person=models.ForeignKey("authentication.person", verbose_name=_("person"), on_delete=models.PROTECT)
    bank=models.ForeignKey("bank", verbose_name=_("bank"), on_delete=models.PROTECT)
    card_no=models.CharField(_("card_no"),max_length=20,null=True,blank=True)
    shaba_no=models.CharField(_("shaba_no"),max_length=50,null=True,blank=True)
    account_no=models.CharField(_("account_no"),max_length=20,null=True,blank=True)
     
    class_name='bankaccount'
    app_name=APP_NAME

    class Meta:
        verbose_name = _("حساب بانکی")
        verbose_name_plural = _("حساب های بانکی")
 
    def save(self,*args, **kwargs):
        
        if self.app_name is None or self.app_name=='':
            self.app_name=APP_NAME
        if self.class_name is None or self.class_name=='':
            self.class_name='bankaccount'
              
              
        result,message,bank_account= super(BankAccount,self).save(*args, **kwargs)
        if result==SUCCEED:
            message='حساب بانکی با موفقیت اضافه شد'
        return result,message,bank_account
 

class Asset(CorePage):
    owner=models.ForeignKey("accounting.personaccount", verbose_name=_("owner"), on_delete=models.PROTECT)
   
    class Meta:
        verbose_name = 'دارایی'
        verbose_name_plural = 'دارایی ها'

    def save(self):
        if self.class_name is None or self.class_name=="":
            self.class_name="asset"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        result,message,self=super(Asset,self).save()
        result,message,asset=SUCCEED,"دارایی با موفقیت افزوده شد.",self
        return result,message,asset
    
    