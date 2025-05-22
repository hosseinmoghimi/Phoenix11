from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL

from django.views import View
from .forms import *
from .apps import APP_NAME
from phoenix.server_apps import phoenix_apps
from utility.calendar import PersianCalendar
from core.views import CoreContext 
from .repo import AccountRepo
from .serializer import AccountSerializer
from utility.currency import to_price_colored
import json 

LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='accounting/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"

def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context


 
class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        phoenix_apps = sorted(phoenix_apps, key=lambda d: d['priority'])

        context['phoenix_apps']=phoenix_apps
        return render(request,TEMPLATE_ROOT+"index.html",context)



class TreeChartView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context[WIDE_LAYOUT]=True
        
        context=getContext(request=request)
        if 'pk' in kwargs and not int(kwargs["pk"])==0:
            account=AccountRepo(request=request).account(*args, **kwargs)

            accounts=account.all_childs()
            context['account']=account
        else:
            accounts=AccountRepo(request=request).list(*args, **kwargs)

        context['accounts']=accounts
        pages=[]
         
        AG=100
        BA=100000
        MA=100000000
        MA2=10000000000
        for account in accounts:
            pages.append({
                'title': f"""{account.code}<br>{account.name}""",
                'parent_id': account.parent_id,
                'parent': 0,
                'get_absolute_url': account.get_absolute_url(),
                'id': account.id,
                'pre_title': "",
                'color': account.color,
                'sub_title':to_price_colored(account.balance),
                })

        context['pages_s'] = json.dumps(pages)
        return render(request,TEMPLATE_ROOT+"tree-chart.html",context) 

 
class AccountsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        phoenix_apps = sorted(phoenix_apps, key=lambda d: d['priority'])

        context['phoenix_apps']=phoenix_apps
        return render(request,TEMPLATE_ROOT+"accounts.html",context)

 
class AccountView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        phoenix_apps = sorted(phoenix_apps, key=lambda d: d['priority'])

        context['phoenix_apps']=phoenix_apps
        return render(request,TEMPLATE_ROOT+"account.html",context)

class SelectionView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        phoenix_apps = sorted(phoenix_apps, key=lambda d: d['priority'])

        context['phoenix_apps']=phoenix_apps
        return render(request,TEMPLATE_ROOT+"selection.html",context)
