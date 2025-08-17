from accounting.forms import forms

class AddBookForm(forms.Form):
    title=forms.CharField(max_length=100,required=True) 
 