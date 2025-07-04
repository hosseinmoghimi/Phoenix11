from django import forms

class TogglePageLikeForm(forms.Form):
    page_id=forms.IntegerField(required=True)
 