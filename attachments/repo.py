from core.repo import PageRepo,ProfileRepo
from .models import Like

class LikeRepo():
    def __init__(self,request,*args, **kwargs):
        self.objects=Like.objects
        self.request=request
    def toggle_like(self,*args, **kwargs):
        page=PageRepo(request=self.request).page(*args, **kwargs)
        if page is None:
            return None
        me_profile=ProfileRepo(request=self.request).me
        if me_profile is None:
            return None
        likes=Like.objects.filter(page_id=page.id).filter(profile_id=me_profile.id)
        my_like=False
        if len(likes)==0:
            my_like=Like(page=page,profile=me_profile)
            my_like.save()
            my_like=True
        else:
            likes.delete()
        likes_count=self.likes_count(page=page)
        return (my_like,likes_count)
    

    def my_like(self,*args, **kwargs):
        profile_me=ProfileRepo(request=self.request).me
        page=PageRepo(request=self.request).page(*args, **kwargs)
        if profile_me is None:
            return None
        if page is None:
            return None
        likes=Like.objects.filter(profile_id=profile_me.id).filter(page_id=page.id)
        return len(likes)>0
    
    def likes_count(self,*args, **kwargs):
        page=PageRepo(request=self.request).page(*args, **kwargs)
        if page is None:
            return None
        return len(Like.objects.filter(page_id=page.pk))    