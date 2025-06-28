from .models import Page,Like
from authentication.repo import ProfileRepo

class PageRepo():
    def __init__(self,request,*args, **kwargs):
        self.objects=Page.objects
        self.request=request
    def page(self,*args, **kwargs):
        page=None
        if 'page_id' in kwargs:
            page=self.objects.filter(pk=kwargs['page_id']).first()
        if 'pk' in kwargs:
            page=self.objects.filter(pk=kwargs['pk']).first()
        return page
    def toggle_like(self,*args, **kwargs):
        page=self.page(*args, **kwargs)
        if page is None:
            return None
        profile=ProfileRepo(request=self.request).me
        likes=Like.objects.filter(page_id=page.id).filter(profile_id=profile.id)
        my_like=False
        if len(likes)==0 and profile is not None and page is not None:
            my_like=Like(page=page,profile=profile)
            my_like.save()
            my_like=True
        else:
            likes.delete()
        likes_count=page.likes_count
        return (my_like,likes_count)