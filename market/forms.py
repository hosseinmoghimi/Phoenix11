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
