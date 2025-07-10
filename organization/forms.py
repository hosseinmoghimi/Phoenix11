from accounting.forms import AddProductForm,forms
 
class AddOrganizationUnitForm(forms.Form):
    title=forms.CharField(max_length=50,required=True)
    account_id=forms.IntegerField(required=True)
    
 