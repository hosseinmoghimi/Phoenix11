from .server_settings import SITE_URL,STATIC_URL
phoenix_apps=[
    
    {'priority':1,'name':'core','url':SITE_URL+'','title':'خانه','logo':STATIC_URL+'core'+'/img/'+'logo.png','color':'warning',},
    {'priority':2,'name':'accounting','url':SITE_URL+'accounting/','title':'حسابداری','logo':STATIC_URL+'accounting'+'/img/'+'logo.png','color':'success',},
    {'priority':2,'name':'projectmanager','url':SITE_URL+'pm/','title':'مدیریت پروژه','logo':STATIC_URL+'projectmanager'+'/img/'+'logo.png','color':'info',},
    {'priority':3,'name':'market','url':SITE_URL+'market/','title':'فروشگاه','logo':STATIC_URL+'market'+'/img/'+'logo.png','color':'danger',},
    {'priority':4,'name':'authentication','url':SITE_URL+'authentication/','title':'هویت','logo':STATIC_URL+'authentication'+'/img/'+'logo.png','color':'success',},
    {'priority':5,'name':'utility','url':SITE_URL+'utility/','title':'ابزار های کاربردی','logo':STATIC_URL+'utility'+'/img/'+'logo.png','color':'info',},
    {'priority':5,'name':'warehouse','url':SITE_URL+'warehouse/','title':'انبارداری','logo':STATIC_URL+'warehouse'+'/img/'+'logo.png','color':'success',},
    {'priority':6,'name':'log','url':SITE_URL+'log/','title':'لاگ','logo':STATIC_URL+'log'+'/img/'+'logo.png','color':'warning',},
    {'priority':7,'name':'chef','url':SITE_URL+'chef/','title':'سرآشپز','logo':STATIC_URL+'chef'+'/img/'+'logo.png','color':'primary',},
    {'priority':4,'name':'attachments','url':SITE_URL+'attachments/','title':'اطلاعات پیوستی','logo':STATIC_URL+'attachments'+'/img/'+'logo.png','color':'info',},
    {'priority':8,'name':'archive','url':SITE_URL+'archive/','title':'آرشیو','logo':STATIC_URL+'archive'+'/img/'+'logo.png','color':'info',},
    {'priority':8,'name':'messenger','url':SITE_URL+'messenger/','title':'پیام رسان','logo':STATIC_URL+'messenger'+'/img/'+'logo.png','color':'primary',},
    {'priority':9,'name':'organization','url':SITE_URL+'organization/','title':'مدیریت سازمانی','logo':STATIC_URL+'organization'+'/img/'+'logo.png','color':'primary',},
    {'priority':10,'name':'school','url':SITE_URL+'school/','title':'آموزشگاه','logo':STATIC_URL+'school'+'/img/'+'logo.png','color':'danger',},
    {'priority':10,'name':'transport','url':SITE_URL+'transport/','title':'حمل و نقل','logo':STATIC_URL+'transport'+'/img/'+'logo.png','color':'primary',},
    {'priority':11,'name':'bms','url':SITE_URL+'bms/','title':'هوشمند سازی','logo':STATIC_URL+'bms'+'/img/'+'logo.png','color':'info',},
    {'priority':4,'name':'resume','url':SITE_URL+'resume/','title':'رزومه','logo':STATIC_URL+'resume'+'/img/'+'logo.png','color':'success',},
    {'priority':4,'name':'tax','url':SITE_URL+'tax/','title':'مالیات','logo':STATIC_URL+'tax'+'/img/'+'logo.png','color':'warning',},
    {'priority':12,'name':'blog','url':SITE_URL+'blog/','title':'بلاگ','logo':STATIC_URL+'blog'+'/img/'+'logo.png','color':'warning',},

]