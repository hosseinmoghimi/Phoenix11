from accounting.forms import AddProductForm,forms

class AddTableForm(forms.Form):
    table_no=forms.IntegerField(required=True)
    title=forms.CharField(max_length=50,required=True)
