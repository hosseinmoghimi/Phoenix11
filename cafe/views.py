from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from .repo import TableRepo
from .serializers import TableSerializer
from django.views import View
from .forms import *
from .apps import APP_NAME
from core.views import CoreContext
from phoenix.server_apps import phoenix_apps
from utility.calendar import PersianCalendar
import json

from .serializers import MenuSerializer,DeskCustomerSerializer,DeskSerializer
from .repo import MenuRepo,DeskRepo,DeskCustomerRepo

from utility.enums import UnitNameEnum
from utility.log import leolog
from accounting.views import AddInvoiceLineContext,InvoiceContext,ProductContext
LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='cafe/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"
 
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context

def AddDeskContext(request,*args, **kwargs):
    context={}
    from market.views import SupplierRepo,SupplierSerializer
    suppliers=SupplierRepo(request=request).list()
    suppliers_s=json.dumps(SupplierSerializer(suppliers,many=True).data)
    context['suppliers_s']=suppliers_s
    context['suppliers']=suppliers
    return context

def AddMenuContext(request,*args, **kwargs):
    context={}
    from market.views import SupplierRepo,SupplierSerializer
    suppliers=SupplierRepo(request=request).list()
    suppliers_s=json.dumps(SupplierSerializer(suppliers,many=True).data)
    context['suppliers_s']=suppliers_s
    context['suppliers']=suppliers
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
# Create your views here. 

 
 
class TablesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        tables=TableRepo(request=request).list(*args, **kwargs)
        context["tables"]=tables
        tables_s=json.dumps(TableSerializer(tables,many=True).data)
        context["tables_s"]=tables_s

        if request.user.has_perm(APP_NAME+".add_table"):
            context['add_table_form']=AddTableForm()
        return render(request,TEMPLATE_ROOT+"tables.html",context)
# Create your views here. 

 
class TableView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        table=TableRepo(request=request).table(*args, **kwargs)
        table_s=json.dumps(TableSerializer(table,many=False).data)
        context["table_s"]=table_s
        context["table"]=table
        leolog(table=table,id=table.id,pk=table.pk)
        return render(request,TEMPLATE_ROOT+"table.html",context)
# Create your views here. 
 

   
    
class DeskView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        desk =DeskRepo(request=request).desk(*args, **kwargs)
        context['desk']=desk
        
        menus=desk.supplier.menu_set.all()
        menus_s=json.dumps(MenuSerializer(menus,many=True).data)
        context['menus']=menus
        context['menus_s']=menus_s
 
  
        context['NOT_NAVBAR']=True
        context['NOT_FOOTER']=True
        return render(request,TEMPLATE_ROOT+"desk.html",context) 
    
    
class DeskMenuView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        from market.views import ShopSerializer
        desk =DeskRepo(request=request).desk(*args, **kwargs)
        menu =MenuRepo(request=request).menu(*args, **kwargs)
        context['desk']=desk
        context['menu']=menu
        
        
        desk_customer=DeskCustomerRepo(request=request).desk_customer(desk_id=desk.id)
        context['desk_customer']=desk_customer

        desk_customer_s=json.dumps(DeskCustomerSerializer(desk_customer,many=False).data)
        menu_s=json.dumps(MenuSerializer(menu,many=False).data)
        context['desk_customer_s']=desk_customer_s
        context['menu_s']=menu_s



        shops=menu.shops.all()
        shops_s=json.dumps(ShopSerializer(shops,many=True).data)
        
        
        context['shops_s']=shops_s
 
        context['NOT_NAVBAR']=True
        context['NOT_FOOTER']=True
        return render(request,TEMPLATE_ROOT+"desk-menu.html",context) 

class DesksView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        desks =DeskRepo(request=request).list(*args, **kwargs)
        context['desks']=desks
        
        desks_s=json.dumps(DeskSerializer(desks,many=True).data)
        context['desks_s']=desks_s
        if request.user.has_perm(APP_NAME+'.add_desk'):
            context['add_desk_form']=AddDeskForm()
            context.update(AddDeskContext(request=request))
        return render(request,TEMPLATE_ROOT+"desks.html",context) 
    

class MenusView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        menus =MenuRepo(request=request).list(*args, **kwargs)
        context['menus']=menus
        menus_s=json.dumps(MenuSerializer(menus,many=True).data)
        context['menus_s']=menus_s
 
        context[WIDE_LAYOUT]=True
        if request.user.has_perm(APP_NAME+".add_menu"):
            context['add_menu_form']=AddMenuForm()
            from market.views import SupplierRepo

            suppliers=SupplierRepo(request=request).list()
            context['suppliers']=suppliers
        return render(request,TEMPLATE_ROOT+"menus.html",context) 
    

class MenuView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        from market.views import CustomerRepo,CartItemRepo,ShopSerializer
        menu =MenuRepo(request=request).menu(*args, **kwargs) 
        context['menu']=menu
        menu_s=json.dumps(MenuSerializer(menu,many=False).data)
        context['menu_s']=menu_s

        shops=menu.shops.all()
        shops_s=json.dumps(ShopSerializer(shops,many=True).data)
        context['shops_s']=shops_s


        from .serializers import MenuItemSerializer,MenuItem
        menu_items=[]
        cart_item_repo=CartItemRepo(request=request)
        me_customer=CustomerRepo(request=request).me
        if me_customer is not None:
            cart_items=cart_item_repo.list(customer_id=me_customer.id)
            pass
        else:
            cart_items=None

        for shop in shops:
            in_cart=0
            menu_item=MenuItem()
            menu_item.shop=shop
            menu_item.in_cart=in_cart
            if cart_items is not None:
                for cart_item in cart_items.filter(shop_id=shop.id):
                    in_cart=cart_item.quantity
                    menu_item.in_cart=in_cart
            menu_items.append(menu_item)


        menu_items_s=json.dumps(MenuItemSerializer(menu_items,many=True).data)
        context['menu_items_s']=menu_items_s

        context[WIDE_LAYOUT]=True
        # context['NOT_NAVBAR']=True
        # context['NOT_FOOTER']=True
        return render(request,TEMPLATE_ROOT+"menu.html",context) 
    
class DeskCustomerView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        from market.views import CustomerRepo,CartItemRepo,ShopSerializer
        menu =MenuRepo(request=request).menu(*args, **kwargs) 
        context['menu']=menu
        menu_s=json.dumps(MenuSerializer(menu,many=False).data)
        context['menu_s']=menu_s

        shops=menu.shops.all()
        shops_s=json.dumps(ShopSerializer(shops,many=True).data)
        context['shops_s']=shops_s


        from .serializers import MenuItemSerializer,MenuItem
        menu_items=[]
        cart_item_repo=CartItemRepo(request=request)
        me_customer=CustomerRepo(request=request).me
        if me_customer is not None:
            cart_items=cart_item_repo.list(customer_id=me_customer.id)
            pass
        else:
            cart_items=None

        for shop in shops:
            in_cart=0
            menu_item=MenuItem()
            menu_item.shop=shop
            menu_item.in_cart=in_cart
            if cart_items is not None:
                for cart_item in cart_items.filter(shop_id=shop.id):
                    in_cart=cart_item.quantity
                    menu_item.in_cart=in_cart
            menu_items.append(menu_item)


        menu_items_s=json.dumps(MenuItemSerializer(menu_items,many=True).data)
        context['menu_items_s']=menu_items_s

        context[WIDE_LAYOUT]=True
        # context['NOT_NAVBAR']=True
        # context['NOT_FOOTER']=True
        return render(request,TEMPLATE_ROOT+"menu.html",context) 
    