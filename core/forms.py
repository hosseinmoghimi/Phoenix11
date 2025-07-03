from django import forms

class TogglePageLikeForm(forms.Form):
    page_id=forms.IntegerField(required=True)

class SetPageThumbnailHeaderForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    clear_thumbnail=forms.BooleanField(required=False)
    clear_header=forms.BooleanField(required=False)