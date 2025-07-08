from core.repo import PageRepo,ProfileRepo,FAILED,SUCCEED
from .models import Like,Comment,Link,Download,Image
from .apps import APP_NAME


class ImageRepo():

    def __init__(self,request,*args, **kwargs):
        self.objects=Image.objects
        self.request=request
    def list(self,*args, **kwargs):
        objects=Image.objects
        if 'page_id' in kwargs:
            objects=objects.filter(page_id=kwargs['page_id'])
        return objects.all()
    def image(self,*args, **kwargs):
        if 'pk' in kwargs and kwargs['pk'] is not None:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs and kwargs['id'] is not None:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'image_id' in kwargs and kwargs['image_id'] is not None:
            return self.objects.filter(pk=kwargs['image_id']).first()
    def add_image(self,*args, **kwargs):
        result,message,image=FAILED,"",None
        profile_me=ProfileRepo(request=self.request).me
        page=PageRepo(request=self.request).page(*args, **kwargs)
        if profile_me is None:
            return None
        if page is None:
            return None
        if 'image' in kwargs:
            image_text=kwargs['image']
        if image_text is None:
            return result,message,image
        image=Image(creator_id=profile_me.id,page_id=page.id,image_main_origin=image_text)
        image.save()
        result=SUCCEED
        message='کامنت با موفقیت اضافه شد.'
        return result,message,image
    
    def delete_image(self,*args, **kwargs):
        profile_me=ProfileRepo(request=self.request).me
        if 'image_id' in kwargs:
            image_id=kwargs['image_id']
        # images=Image.objects.filter(profile_id=profile_me.id).filter(pk=image_id)
        images=Image.objects.filter(pk=image_id)
        images.delete()
        from utility.log import leolog
        result=SUCCEED
        message="کامنت با موفقیت حذف گردید."
        return result,message
     

class CommentRepo():

    def __init__(self,request,*args, **kwargs):
        self.objects=Comment.objects
        self.request=request
    def list(self,*args, **kwargs):
        objects=Comment.objects
        if 'page_id' in kwargs:
            objects=objects.filter(page_id=kwargs['page_id'])
        return objects.all()

    def add_comment(self,*args, **kwargs):
        result,message,comment=FAILED,"",None
        profile_me=ProfileRepo(request=self.request).me
        page=PageRepo(request=self.request).page(*args, **kwargs)
        if profile_me is None:
            return None
        if page is None:
            return None
        if 'comment' in kwargs:
            comment_text=kwargs['comment']
        if comment_text is None:
            return result,message,comment
        comment=Comment(profile_id=profile_me.id,page_id=page.id,comment=comment_text)
        comment.save()
        result=SUCCEED
        message='کامنت با موفقیت اضافه شد.'
        return result,message,comment
    
    def delete_page_comment(self,*args, **kwargs):
        profile_me=ProfileRepo(request=self.request).me
        if 'comment_id' in kwargs:
            comment_id=kwargs['comment_id']
        # comments=Comment.objects.filter(profile_id=profile_me.id).filter(pk=comment_id)
        comments=Comment.objects.filter(pk=comment_id)
        comments.delete()
        from utility.log import leolog
        result=SUCCEED
        message="کامنت با موفقیت حذف گردید."
        return result,message
     
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
    


class LinkRepo():
    def __init__(self,request,*args, **kwargs):
        self.objects=Link.objects
        self.request=request
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'page_id' in kwargs:
            page_id=kwargs['page_id']
            objects=objects.filter(page_id=page_id)
        return objects.all()
    def add_link(self,*args, **kwargs):
        result,message,link=FAILED,'',None
        result=SUCCEED
        link=Link(**kwargs)
        # link.url=url
        # link.title=title
        # link.page_id=page_id
        link.save()
        message='لینک با موفقیت اضافه شد.'
        return result,message,link 

class DownloadRepo():
    def __init__(self,request,*args, **kwargs):
        self.objects=Download.objects
        self.request=request
    def download(self,*args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'download_id' in kwargs:
            return self.objects.filter(pk=kwargs['download_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'page_id' in kwargs:
            page_id=kwargs['page_id']
            objects=objects.filter(page_id=page_id)
        return objects.all()
     
    


    def add_download(self,title,file,priority=1000,*args, **kwargs):
        result,message,download=FAILED,'',None
        can_write=False
        page=PageRepo(request=self.request).page(page_id=kwargs['page_id'])
         
        if self.request.user.has_perm(APP_NAME+".change_page"):
            can_write=True
         
        if page is None or not can_write:
            message='صفحه وجود ندارد.'
            return result,message,download

        if page.app_name=='web':
            is_open=True
        else:
            is_open=False
        me_profile=ProfileRepo(request=self.request).me
        if me_profile is None:
            message='پروفایل وجود ندارد.'
            return result,message,download
        download=Download(icon_fa="fa fa-download",title=title,is_open=is_open,file=file,priority=priority,page_id=page.id,profile_id=me_profile.id)
        download.save()
        result=SUCCEED
        message='دانلود با موفقیت اضافه شد.'
        download.profiles.add(me_profile)
        return result,message,download


