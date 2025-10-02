from accounting.forms import forms

class AddPollForm(forms.Form):
    title=forms.CharField(max_length=100,required=True) 
 