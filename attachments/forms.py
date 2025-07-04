from django import forms

class TogglePageLikeForm(forms.Form):
    page_id=forms.IntegerField(required=True)
 
class AddPageCommentForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    comment=forms.CharField(max_length=5000,required=True)
 
class DeletePageCommentForm(forms.Form):
    comment_id=forms.IntegerField(required=True)
 