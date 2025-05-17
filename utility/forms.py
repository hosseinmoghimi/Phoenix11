from django import forms
class DateTimeForm(forms.Form):
    gregorian_datetime=forms.CharField(max_length=20, required=False)
    persian_datetime=forms.CharField(max_length=20, required=False)
class ReadExcelFileForm(forms.Form):
    title=forms.CharField(max_length=20, required=True)