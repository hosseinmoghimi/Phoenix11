from django import forms

class AddMenuForm(forms.Form):
    title=forms.CharField( max_length=100, required=True)
    supplier_id=forms.IntegerField( required=True)
    
class AddShopToMenuForm(forms.Form):
    title=forms.CharField( max_length=100, required=True)
    supplier_id=forms.IntegerField( required=True)

    
class AddShopForm(forms.Form):
    unit_name=forms.CharField( max_length=100, required=True)
    unit_price=forms.IntegerField( required=True)
    available=forms.IntegerField( required=True)
    product_id=forms.IntegerField( required=True)
    supplier_id=forms.IntegerField( required=True)
    menu_id=forms.IntegerField( required=False)
    menu_title=forms.CharField( max_length=100, required=False)

class AddMarketPersonForm(forms.Form):
    level=forms.CharField(max_length=100, required=False)
    first_name=forms.CharField(max_length=100, required=False)
    last_name=forms.CharField(max_length=100, required=False)
    email=forms.CharField(max_length=100, required=False)
    bio=forms.CharField(max_length=100, required=False)
    mobile=forms.CharField(max_length=100, required=False)
    prefix=forms.CharField(max_length=100, required=False)
    type=forms.CharField(max_length=100, required=False)
    person_id=forms.IntegerField(required=True)
    address=forms.CharField(max_length=100, required=False)
    balance=forms.IntegerField(required=False) 
    code=forms.CharField(max_length=100, required=True)


class AddCustomerForm(AddMarketPersonForm):
    person_account_categories=forms.CharField(max_length=200, required=False)

class AddShipperForm(AddMarketPersonForm):
    person_account_categories=forms.CharField(max_length=200, required=False)

 
class AddSupplierForm(AddMarketPersonForm):
    person_account_categories=forms.CharField(max_length=200, required=False)

class AddSupplierByPersonForm(forms.Form):
    level=forms.CharField(max_length=100, required=False)
    person_id=forms.IntegerField(required=True)  
     

