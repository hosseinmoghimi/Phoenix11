from django import forms

class TogglePageLikeForm(forms.Form):
    page_id=forms.IntegerField(required=True)
 
class AddPageCommentForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    comment=forms.CharField(max_length=5000,required=True)
 
class DeletePageCommentForm(forms.Form):
    comment_id=forms.IntegerField(required=True)
 
class DeleteImageForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    image_id=forms.IntegerField(required=True)


class AddImageForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=100, required=True)

class AddLinkForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    url=forms.CharField(max_length=5000,required=True)
    title=forms.CharField(max_length=5000,required=True)
    priority=forms.IntegerField(required=False)
 
class AddDownloadForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=5000,required=True)
    priority=forms.IntegerField(required=False)