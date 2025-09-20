from django import forms
from attachments.forms import AddLinkForm
class DateTimeForm(forms.Form):
    gregorian_datetime=forms.CharField(max_length=20, required=False)
    persian_datetime=forms.CharField(max_length=20, required=False)
class ReadExcelFileForm(forms.Form):
    title=forms.CharField(max_length=20, required=True)

class SearchForm(forms.Form):
    app_name=forms.CharField(max_length=50,required=True)
    search_for=forms.CharField(max_length=100, required=True)

class AddToClipBoradForm(forms.Form):
    name=forms.CharField(max_length=100,required=True)
    text=forms.CharField(max_length=100,required=True)
    
class DeleteMyLinkForm(forms.Form):
    my_link_id=forms.IntegerField(required=True)
    
class AddMyLinkForm(forms.Form):
    url=forms.CharField(max_length=5000,required=True)
    title=forms.CharField(max_length=5000,required=True)
    priority=forms.IntegerField(required=False)    
    
class GetParametersForm(forms.Form):
    app_name=forms.CharField(max_length=50,required=True)
    
class SetParameterForm(forms.Form): 
    app_name=forms.CharField(max_length=50,required=True)
    name=forms.CharField(max_length=100,required=True)
    value=forms.CharField(max_length=10000,required=True)
