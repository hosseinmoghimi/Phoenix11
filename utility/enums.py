from django.utils.translation import gettext as _
from django.db.models import TextChoices
 
 
 
class WeightUnitEnum(TextChoices):
    KILO_GRAM="کیلوگرم",_("کیلوگرم")
    GRAM="گرم",_("گرم")
    TON="تن",_("تن")

class UnitNameEnum(TextChoices):
    ADAD="عدد",_("عدد")
    KILOGERAM="کیلوگرم",_("کیلوگرم")
    METER="متر",_("متر")
    SHAKHEH="شاخه",_("شاخه")
    SHISHEH="شیشه",_("شیشه")
    DASTGAH="دستگاه",_("دستگاه")
    GERAM="گرم",_("گرم")
    SHEET="ورق",_("ورق")
    TON="تن",_("تن")
    LINE="خط",_("خط")
    PORS="پورس",_("پورس")
    METER2="متر مربع",_("متر مربع")
    METER3="متر مکعب",_("متر مکعب")
    PART="قطعه",_("قطعه")
    Roll="رول",_("رول")
    DAY="روز",_("روز")
    TAKHTE="تخته",_("تخته")
    LINK="لینک",_("لینک")
    SERVICE="سرویس",_("سرویس")
    INSTANCE="مورد",_("مورد")
    PERSON="نفر",_("نفر")
    PACK="بسته",_("بسته")
    POCKET="کیسه",_("کیسه")
    SHOT="شات",_("شات")
    SET="ست",_("ست")
    CUP="فنجان",_("فنجان")
    JOFT="جفت",_("جفت")
    DAST="دست",_("دست")
    CARTON="کارتن",_("کارتن")
    HOUR="ساعت",_("ساعت")
    MINUTE="دقیقه",_("دقیقه")
    JABE="جعبه",_("جعبه")
    SABAD="سبد",_("سبد")
    RAS="راس",_("راس")
    BOTTLE="بطری",_("بطری")


class OperatingSystemNameEnum(TextChoices):
    WIN_SERVER_2012='Windows Server 2012',_('Windows Server 2012')
    WIN_SERVER_2018='Windows Server 2018',_('Windows Server 2018')
    WIN_SERVER_2020='Windows Server 2020',_('Windows Server 2020')
    WIN_SERVER_2022='Windows Server 2022',_('Windows Server 2022')
    WIN_SERVER_2024='Windows Server 2024',_('Windows Server 2024')
    LINUX='Linux',_('Linux')
    LINUX_UBUNTU='Linux Ubuntu',_('Linux Ubuntu')
    LINUX_UBUNTU_24='Linux Ubuntu 2024',_('Linux Ubuntu 2024')
    ANDROID='ANDROID',_('ANDROID')
    IOS='IOS',_('IOS')
    Ltr='ltr',_('ltr')
  
class TextDirectionEnum(TextChoices):
    Rtl='rtl',_('rtl')
    Ltr='ltr',_('ltr')

def BS_ColorCode(bs_color):
    if bs_color=='success':
        return "#28a745"
    if bs_color=='danger':
        return "#dc3545"
    if bs_color=='warning':
        return "#ffc107"
    if bs_color=='muted':
        return "#34345455"
    if bs_color=='info':
        return "#17a2b8"
    if bs_color=='rose':
        return "#34345455"
    if bs_color=='secondary':
        return "#6c757d"
    if bs_color=='light':
        return "#f8f9fa"
    if bs_color=='dark':
        return "#343a40"
    if bs_color=='primary':
        return "#007bff"
    if bs_color=='blue':
        return "#007bff"
    if bs_color=='indigo':
        return "#6610f2"
    if bs_color=='purple':
        return "#6f42c1"
    if bs_color=='pink':
        return "#e83e8c"
    if bs_color=='red':
        return "#dc3545"
    if bs_color=='orange':
        return "#fd7e14"
    if bs_color=='yellow':
        return "#ffc107"
    if bs_color=='green':
        return "#28a745"
    if bs_color=='teal':
        return "#20c997"
    if bs_color=='cyan':
        return "#17a2b8"
    if bs_color=='white':
        return "#fff"
    if bs_color=='gray':
        return "#6c757d"
    if bs_color=='gray-dark':
        return "#343a40"


  
class GenderEnum(TextChoices):
    MALE="مرد" , _("مرد")
    FEMALE="زن" , _("زن")
    OTHERS="دیگر" , _("دیگر")

    
class PersonPrefixEnum(TextChoices):
    MR="آقای",_("آقای")
    MRS="خانم",_("خانم")
    COMPANY="شرکت",_("شرکت")
    DR="دکتر",_("دکتر")
    ENGINEER="مهندس",_("مهندس")
    COMPLEX=" مجتمع",_(" مجتمع")
  
class AppNameEnum(TextChoices):
    projectmanager='projectmanager',_('projectmanager')
    accounting='accounting',_('accounting')
    web='web',_('web')
    transport='transport',_('transport')
    log='log',_('log')
    map='map',_('map')
    market='market',_('market')
    stock='stock',_('stock')
    authentication='authentication',_('authentication')
    dashboard='dashboard',_('dashboard')
    polls='polls',_('polls')
 

class LanguageEnum(TextChoices):
    FARSI="فارسی",_("فارسی")
    ENGLISH="انگلیسی",_("انگلیسی")
    
def LanguageCode(language):
    if language==LanguageEnum.FARSI:
        return 'fa'
    if language==LanguageEnum.ENGLISH:
        return 'en'
def LanguageFromCode(code):
    if code=='fa':
        return LanguageEnum.FARSI
    if code=='en':
        return LanguageEnum.ENGLISH
   
class PictureNameEnum(TextChoices):
    LOGO="لوگو",_("لوگو")
    FAVICON="آیکون",_("آیکون")
    BACKGROUND="پس زمینه",_("پس زمینه")
    APP_BACKGROUND_IMAGE="تصویر پس زمینه اپ",_("تصویر پس زمینه اپ")
    
class ColorEnum(TextChoices):
    SUCCESS = 'success', _('success')
    DANGER = 'danger', _('danger')
    WARNING = 'warning', _('warning')
    PRIMARY = 'primary', _('primary')
    MUTED = 'muted', _('muted')
    SECONDARY = 'secondary', _('secondary')
    INFO = 'info', _('info')
    LIGHT = 'light', _('light')
    ROSE = 'rose', _('rose')
    DARK = 'dark', _('dark') 





def class_title(*args, **kwargs):
    class_name='page'
    app_name='core'
    if 'class_name' in kwargs:
        class_name=kwargs['class_name']
    if 'app_name' in kwargs:
        app_name=kwargs['app_name']

    class_title = "صفحه"
    if class_name == "exam":
        class_title = "آزمون"
    if class_name == "pricingpage":
        class_title = "لیست قیمت"
    if class_name == "poll":
        class_title = "پرسش"
    if class_name == "account":
        class_title = "حساب"
    if class_name == "payment":
        class_title = "پرداخت"
    if class_name == "property":
        class_title = "ملک"
    if class_name == "book":
        class_title = "کتاب"
    if class_name == "page":
        class_title = "صفحه"
    if class_name == "appointment":
        class_title = "قرار ملاقات"
    if class_name == "coupon":
        class_title = "جایزه خرید"
    if class_name == "letter":
        class_title = "نامه"
    if class_name == "file":
        class_title = "فایل"
    if class_name == "ourwork":
        class_title = "پروژه"
    if class_name == "feature":
        class_title = "خدمات"
    if class_name == "blog":
        class_title = "مقاله"
    if class_name == "material":
        class_title = "متریال"
    if class_name == "product":
        class_title = "کالا"
    if class_name == "vehicle":
        class_title = "وسیله نقلیه"
    if class_name == "project":
        class_title = "پروژه"
    if class_name == "cost":
        class_title = "هزینه"
    if class_name == "service":
        class_title = "سرویس"
    if class_name=="pm_service":
        class_title = "سرویس"
    if class_name=="luggage":
        class_title = "محموله بار"
    if class_name == "organizationunit":
        class_title = "واحد سازمانی"
    if class_name == "event":
        class_title = "رویداد"
    if class_name=="invoice":
        class_title= "فاکتور"
    if class_name=="maintenance":
        class_title= "تعمیر و نگهداری"
    if class_name=="materialinvoice":
        class_title= "فاکتور متریال"
    if class_name=="serviceinvoice":
        class_title ="فاکتور خدمات"
    if class_name=="workshift":
        class_title= "شیفت کاری"
    if class_name=="fooditem":
        class_title= "آیتم غذایی"
    if class_name=="role":
        class_title= "نقش"
    if class_name=="financialdocument":
        class_title= "سند مالی"
    if class_name=="financialevent":
        class_title= "رویداد مالی"
    return class_title
class ParameterNameEnum(TextChoices):
    VISITOR_COUNTER="تعداد بازدید",_("تعداد بازدید")
    CURRENCY="واحد پول",_("واحد پول")
    TITLE="عنوان",_("عنوان")
    FARSI_FONT_NAME="نام فونت فارسی",_("نام فونت فارسی")
    HOME_URL="لینک به خانه",_("لینک به خانه")
    THUMBNAIL_DIMENSION="عرض تصاویر کوچک",_("عرض تصاویر کوچک")
    ONLY_HTTPS="فقط https",_("فقط https")
    SHOW_ARCHIVES="نمایش فایل های آرشیو شده",_("نمایش فایل های آرشیو شده")
    HAS_APP_BACKGROUND="اپ تصویر زمینه دارد؟",_("اپ تصویر زمینه دارد؟")