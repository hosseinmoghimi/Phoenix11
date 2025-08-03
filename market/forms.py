from django import forms

class AddMenuForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
    supplier_id=forms.IntegerField(required=True)
    
class AddShopToMenuForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
    supplier_id=forms.IntegerField(required=True)

    
class AddShopForm(forms.Form):
    level=forms.CharField(max_length=100, required=True)
    unit_name=forms.CharField(max_length=100, required=True)
    unit_price=forms.IntegerField(required=True)
    available=forms.IntegerField(required=True)
    product_id=forms.IntegerField(required=True)
    supplier_id=forms.IntegerField(required=False)
    coef=forms.IntegerField(required=False)
    discount_percentage=forms.IntegerField(required=False)
    menu_id=forms.IntegerField(required=False)
    menu_title=forms.CharField(max_length=100, required=False)
    start_date=forms.CharField(max_length=100, required=False)
    end_date=forms.CharField(max_length=100, required=False)
    
class CheckoutCartForm(forms.Form):
    address=forms.CharField(max_length=100, required=True)
    postal_code=forms.CharField(max_length=100, required=True)

class AddCartItemForm(forms.Form):
    unit_name=forms.CharField(max_length=100, required=False)
    shop_id=forms.IntegerField(required=True)
    quantity=forms.IntegerField(required=False)
    
class AddMarketPersonForm(forms.Form):
    level=forms.CharField(max_length=100, required=False)
    person_account_id=forms.IntegerField(required=True)
   
class AddCartLineForm(forms.Form):
    shop_id=forms.IntegerField(required=True)
   


class AddCustomerForm(AddMarketPersonForm):
    person_account_categories=forms.CharField(max_length=200, required=False)

class AddShipperForm(AddMarketPersonForm):
    person_account_categories=forms.CharField(max_length=200, required=False)

 
class AddSupplierForm(AddMarketPersonForm):
    person_account_categories=forms.CharField(max_length=200, required=False)

class AddSupplierByPersonForm(forms.Form):
    level=forms.CharField(max_length=100, required=False)
    person_id=forms.IntegerField(required=True)  
     

