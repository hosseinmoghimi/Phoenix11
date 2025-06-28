from django import forms
 
class AddSTHForm(forms.Form):
    title=forms.CharField(max_length=50,required=True)
    event_datetime=forms.CharField(max_length=50,required=False)
    bestankar_id=forms.IntegerField(required=True)
    bedehkar_id=forms.IntegerField(required=True)
 