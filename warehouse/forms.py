from accounting.forms import AddProductForm,forms

class AddWareHouseForm(forms.Form):
    name=forms.CharField(max_length=50,required=True)
    account_id=forms.IntegerField(required=True)
 