from accounting.forms import AddProductForm,forms

class AddWareHouseForm(forms.Form):
    name=forms.CharField(max_length=50,required=True)
    person_account_id=forms.IntegerField(required=True) 
 
class AddWareHouseSheetForm(forms.Form):
    invoice_line_id=forms.IntegerField(required=True) 
    warehouse_id=forms.IntegerField(required=True) 
    shelf=forms.CharField(required=True,max_length=50)
    row=forms.CharField(required=True,max_length=50)
    col=forms.CharField(required=True,max_length=50)
    direction=forms.CharField(required=True,max_length=50)
    description=forms.CharField(required=True,max_length=500)
     
class SelectWareHouseForm(forms.Form):
    warehouse_id=forms.IntegerField(required=True) 