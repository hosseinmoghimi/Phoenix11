import jdatetime
import datetime
from  django.utils import timezone
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from .log import leolog

class PersianCalendar():
    def __init__(self,*args, **kwargs):
        self.gdate_time=datetime.now()
        if 'gdate_time' in kwargs:
            self.gdate_time=kwargs['gdate_time']

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
        # if 'gdate_time' in kwargs:
        #     self.gdate_time=kwargs['gdate_time']
        
        

        #     H=self.gdate_time.hour
        #     mm=self.gdate_time.minute
        #     s=self.gdate_time.second

            
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
        return self


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