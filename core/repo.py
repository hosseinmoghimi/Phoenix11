from .models import Page,FAILED,SUCCEED
from authentication.repo import ProfileRepo
from django.db.models import Q
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
        if 'id' in kwargs:
            page=self.objects.filter(pk=kwargs['id']).first()
        return page
    
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'meta_data' in kwargs:
            meta_data=kwargs['meta_data']
            objects=objects.filter(meta_data=meta_data)
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects=objects.filter(Q(title__contains=search_for) |Q(meta_data=search_for))
        return objects.all()
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

    
    