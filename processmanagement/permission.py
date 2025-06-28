from .enums import OperationEnum
class Permission:
    def __init__(self,request,*args, **kwargs):
        self.request=request
    def is_permitted(self,app_name,table,operation):
        if self.request.user.has_perm(f"{app_name}.{operation}_{table}"):
            return True
        return False