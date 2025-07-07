from django import forms

class TogglePageLikeForm(forms.Form):
    page_id=forms.IntegerField(required=True)

class SetPageThumbnailHeaderForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    clear_thumbnail=forms.BooleanField(required=False)
    clear_header=forms.BooleanField(required=False)
class SearchForm(forms.Form):
    search_for=forms.CharField(max_length=50,required=False)
    app_name=forms.CharField(max_length=50,required=False)