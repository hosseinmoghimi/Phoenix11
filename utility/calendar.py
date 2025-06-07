import jdatetime
import datetime
from  django.utils import timezone
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from .log import leolog



HOURS_OFFSET=3
MINUTES_OFFSET=30


DAY_LIGHT_SAVING=False
def to_persian_datetime_tag(value,*args, **kwargs):
    if 'pure_text' in kwargs and kwargs['pure_text']==True:
        return f"""
        {date_} {time_}
        """
    try:    
        a=str(PersianCalendar().from_gregorian(value))
        date_=a[:10]
        time_=a[11:]
        greg=value.strftime("%Y/%m/%d %H:%M:%S") 
        return f"""<span class="ltr" title="{greg}">{date_} <small class="mx-1 text-muted">{time_}</small></span>"""
    except:
        return ""

PERSIAN_MONTH_NAMES=[
'',
'فروردین',
'اردیبهشت',
'خرداد',
'تیر',
'مرداد',
'شهریور',
'مهر',
'آبان',
'آذر',
 'دی',
 'بهمن',
 'اسفند'
]

class DateHelper():
    def persian_start_date(self):
        return PersianCalendar().from_gregorian(self.start_date)[:10]
    def persian_start_datetime(self):
        return PersianCalendar().from_gregorian(self.start_datetime)
    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)
    def persian_end_date(self):
        return PersianCalendar().from_gregorian(self.end_date)[:10]
    def persian_end_datetime(self):
        return PersianCalendar().from_gregorian(self.end_datetime)
    def persian_date(self):
        return PersianCalendar().from_gregorian(self.date)[:10]
    


def to_persian_month_name(month):
    # return PERSIAN_MONTH_NAMES[month]
    if month>-1 and month<12:
        return PERSIAN_MONTH_NAMES[month]
    return "نامعتبر"

def days_in_month(year,month,day=1):
    nn=JalaliDate(year=year,month=month,day=day)
    return nn.daysinmonth



class PersianCalendar():
    def __init__(self,gdate_time=None,*args, **kwargs):

        if gdate_time is not None:
            self.gdate_time=gdate_time
        else:
            self.gdate_time=datetime.now()


        self.date_time=""
        self.fromgregorian()
 
        if 'end_date' in kwargs:
            
            self.hour=23
            self.minute=59
            self.second=59

        if 'start_date' in kwargs:
            
            self.hour=0
            self.minute=0
            self.second=0


    def fromgregorian(self,*args, **kwargs):  
            
        self.hour=self.gdate_time.hour
        self.minute=self.gdate_time.minute
        self.second=self.gdate_time.second

        D=self.gdate_time.day
        M=self.gdate_time.month
        Y=self.gdate_time.year

        H=self.gdate_time.hour
        mm=self.gdate_time.minute
        s=self.gdate_time.second
   
   
        self.date_time=(jdatetime.date.fromgregorian(day=D,month=M,year=Y,hour=H,minute=mm,second=s))
 
        if 'end_date' in kwargs:
            self.hour=23
            self.minute=59
            self.second=59
        if 'start_date' in kwargs:
            self.hour=0
            self.minute=0
            self.second=0

        return str(self)


    def __str__(self): 
        
        return self.to_datetime()  
    

    def to_date(self,*args,**kwargs):
        ssttrr=""
        Y=self.date_time.year
        M=self.date_time.month if self.date_time.month>9 else "0"+str(self.date_time.month)
        D=self.date_time.day if self.date_time.day>9 else "0"+str(self.date_time.day)
        ssttrr=f'{Y}/{M}/{D}'
        
        return ssttrr
    
    def to_datetime(self,*args,**kwargs):
        ssttrr=""
        Y=self.date_time.year
        M=self.date_time.month if self.date_time.month>9 else "0"+str(self.date_time.month)
        D=self.date_time.day if self.date_time.day>9 else "0"+str(self.date_time.day)

        H=self.hour if self.hour>9 else "0"+str(self.hour)
        mm=self.minute if self.minute>9 else "0"+str(self.minute)
        s=self.second if self.second>9 else "0"+str(self.second)
        ssttrr=f'{Y}/{M}/{D}  {H}:{mm}:{s}'
        
        return ssttrr