from accounting.forms import forms

class AddCatalogForm(forms.Form):
    title=forms.CharField(max_length=100,required=True) 
 