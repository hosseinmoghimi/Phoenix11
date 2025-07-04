from .models import Page,FAILED,SUCCEED
from authentication.repo import ProfileRepo
  
class PageRepo():
    def __init__(self,request,*args, **kwargs):
        self.objects=Page.objects
        self.request=request
    def page(self,*args, **kwargs):
        page=None
        if 'page' in kwargs:
            page=kwargs['page']
            return page
        if 'page_id' in kwargs:
            page=self.objects.filter(pk=kwargs['page_id']).first()
        if 'pk' in kwargs:
            page=self.objects.filter(pk=kwargs['pk']).first()
        return page
    
    
    def set_thumbnail_header(self,*args, **kwargs):
        if not self.request.user.has_perm("core.change_page"):
            return
        page=PageRepo(request=self.request).page(*args, **kwargs)
        if page is None:
            return

        if 'clear_thumbnail' in kwargs and kwargs['clear_thumbnail']:
            page.thumbnail_origin=None
        else:
            if 'thumbnail' in kwargs:
                thumbnail=kwargs['thumbnail']
                if thumbnail is not None:
                    page.thumbnail_origin=thumbnail
                    page.save()



        if 'clear_header' in kwargs and kwargs['clear_header']:
            page.header_origin=None
        else:
            if 'header' in kwargs:
                header=kwargs['header']
                if header is not None:
                    page.header_origin=header
                    page.save()
        return page

    
    