from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from accounting.repo import ProductRepo
from .serializers import ProductSerializer,MenuSerializer,SupplierSerializer,ShopSerializer,DeskSerializer,DeskCustomerSerializer
from .repo import MenuRepo,SupplierRepo,DeskRepo,DeskCustomerRepo,ShopRepo,CustomerRepo,ShipperRepo
from .forms import *
from .apps import APP_NAME
from phoenix.server_apps import phoenix_apps
from utility.calendar import PersianCalendar
from accounting.views import CategoryRepo
import json
from .enums import *
from django.views import View
from core.views import CoreContext,leolog
from authentication.views import PersonRepo,PersonSerializer,AddPersonContext
from utility.enums import PersonPrefixEnum
LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='market/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"
 
        
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
    context[WIDE_LAYOUT]=False 
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context

def AddMarketPersonContext(request):
    context={}
    context['customer_levels']=(i[0] for i in ShopLevelEnum.choices)
    context=AddPersonContext(request=request)
    context['person_prefixs_for_add_supplier_app']=(i[0] for i in PersonPrefixEnum.choices)
    persons=PersonRepo(request=request).list()
    context['persons']=persons
    context['customer_levels']=(i[0] for i in ShopLevelEnum.choices)
 
    return context
def AddSupplierContext(request,*args, **kwargs):
    if not request.user.has_perm(APP_NAME+".add_supplier"):
        return context
    context=AddMarketPersonContext(request=request)
  
    ids=(SupplierRepo(request=request).list().values('person_id'))
    persons=context['persons']
    persons=persons.exclude(id__in=ids)
    persons_s_for_add_supplier_app=json.dumps(PersonSerializer(persons,many=True).data)
    context['persons_s_for_add_supplier_app']=persons_s_for_add_supplier_app
    context['add_supplier_form']=AddSupplierForm()
    return context

def AddCustomerContext(request,*args, **kwargs): 
    if not request.user.has_perm(APP_NAME+".add_customer"):
        return {}
    
    context=AddMarketPersonContext(request=request) 
    persons=context['persons']
    ids=(CustomerRepo(request=request).list().values('person_id'))
    persons=persons.exclude(id__in=ids)
    persons_s_for_add_customer_app=json.dumps(PersonSerializer(persons,many=True).data)
    context['persons_s_for_add_customer_app']=persons_s_for_add_customer_app
    context['add_customer_form']=AddCustomerForm()
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

 

class ProductsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        products =ProductRepo(request=request).list(*args, **kwargs)
        context['products']=products
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s
 
        context[WIDE_LAYOUT]=True
        return render(request,TEMPLATE_ROOT+"products.html",context) 
    
    

class CategoryView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        category_repo=CategoryRepo(request=request)
        category=category_repo.category(*args, **kwargs)
        context['category']=category
        leolog(category=category)
        from .serializers import CategorySerializer
        category_s=json.dumps(CategorySerializer(category,many=False).data)
        context['category_s']=category_s 


        if category is None:
            categories=category_repo.roots()
            context['category_id']=0
            products=[]
        else:
            categories=category_repo.list(parent_id=category.id)
            products=category.products.all()
            context['category_id']=category.id
            # leolog(all_childs_products=category.all_childs_products())

        context['categories']=categories
        categories_s=json.dumps(CategorySerializer(categories,many=True).data)
        context['categories_s']=categories_s


        context['products']=products
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s
 
        return render(request,TEMPLATE_ROOT+"category.html",context)

 

    
class ProductView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        product =ProductRepo(request=request).product(*args, **kwargs)
        context['product']=product
        from accounting.views import ProductContext
        context.update(ProductContext(request=request,product=product))
        context[WIDE_LAYOUT]=True
        primary_shop=ShopRepo(request=request).primary_shop(product=product)
        context['primary_shop']=primary_shop
        return render(request,TEMPLATE_ROOT+"product.html",context) 
    

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
            suppliers=SupplierRepo(request=request).list()
            context['suppliers']=suppliers
        return render(request,TEMPLATE_ROOT+"menus.html",context) 
    
    

    
class MenuView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        menu =MenuRepo(request=request).menu(*args, **kwargs) 
        context['menu']=menu
        menu_s=json.dumps(MenuSerializer(menu,many=False).data)
        context['menu_s']=menu_s

        shops=menu.shops.all()
        shops_s=json.dumps(ShopSerializer(shops,many=True).data)
        context['shops_s']=shops_s
 
        context[WIDE_LAYOUT]=True
        context['NOT_NAVBAR']=True
        context['NOT_FOOTER']=True
        return render(request,TEMPLATE_ROOT+"menu.html",context) 
    
    

    

class SuppliersView(View):
    def get(self,request,*args,**kwargs):
        context=getContext(request=request)
        suppliers=SupplierRepo(request=request).list(*args,**kwargs)
        suppliers_s=json.dumps(SupplierSerializer(suppliers,many=True).data)
        context['suppliers']=suppliers
        context['suppliers_s']=suppliers_s
        
        if request.user.has_perm(APP_NAME+".add_supplier"):
            context.update(AddSupplierContext(request=request))
        return render(request,TEMPLATE_ROOT+"suppliers.html",context) 

        
class SupplierView(View):
    def get(self,request,*args,**kwargs):
        context=getContext(request=request)
        supplier=SupplierRepo(request=request).supplier(*args,**kwargs)
        supplier_s=json.dumps(SupplierSerializer(supplier,many=False).data)
        context['supplier']=supplier
        context['supplier_s']=supplier_s
        context['person']=supplier.person

        
        shops=ShopRepo(request=request).list(supplier_id=supplier.id)
        shops_s=json.dumps(ShopSerializer(shops,many=True).data)
        context['shops']=shops
        context['shops_s']=shops_s

        return render(request,TEMPLATE_ROOT+"supplier.html",context) 

       

    
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
 
 
        return render(request,TEMPLATE_ROOT+"desks.html",context) 
    
    

