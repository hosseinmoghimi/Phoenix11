from .models import Profile


class ProfileRepo():
    def __init__(self,request,*args, **kwargs):
        self.request=request
        self.user=request.user
        self.me=None
        if self.user.is_authenticated:
            self.me=Profile.objects.filter(user=request.user).first()
    def logout(self,*args, **kwargs):
        pass      
    def login(self,*args, **kwargs):
        pass      