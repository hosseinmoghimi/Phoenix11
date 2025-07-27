from authentication.repo import ProfileRepo
from messenger.enums import ParameterEnum
from messenger.serializers import MemberSerializer,NotificationSerializer
from messenger.repo import MemberRepo, MessageRepo,ChannelRepo,NotificationRepo
from django.shortcuts import render
from utility.repo import ParameterRepo
from messenger.apps import APP_NAME
from django.views import View
from core.views import CoreContext
import json

TEMPLATE_ROOT=APP_NAME+"/"
LAYOUT_PARENT='phoenix/layout.html'

def MessengerContext(request,*args, **kwargs):
    context={}
    if 'profile' in kwargs and kwargs['profile'] is not None:
        profile=kwargs['profile']
    else:
        profile=ProfileRepo(request=request).me
        if profile is None:
            context['PUSHER_IS_ENABLE']=False
            return {}
    PUSHER_IS_ENABLE=ParameterRepo(request=request,app_name=APP_NAME).parameter(name=ParameterEnum.PUSHER_IS_ENABLE,default='False').boolean_value
    if PUSHER_IS_ENABLE and profile is not None and profile.member_set.first() is not None:
        context.update(get_member_context(request=request))
        notifications=NotificationRepo(request=request).list(member_id=context['member'].id,read=False)
        notifications_s=json.dumps(NotificationSerializer(notifications,many=True).data)
        context['PUSHER_IS_ENABLE'] = True
        context['notifications_s']=notifications_s
        context['notifications']=notifications
    else:
        context['PUSHER_IS_ENABLE'] = False

    return context
def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    profile=context['profile']
    
    
    context.update(MessengerContext(request=request,profile=profile))
        
    return context
def get_member_context(request,*args, **kwargs):
    context={}
    if 'member' in kwargs:
        member=kwargs['member']
    elif 'member_id' in kwargs:
        member=MemberRepo(request=request).member(*args, **kwargs)
    if 'profile' in kwargs:
        profile=kwargs['profile']
        member=profile.member_set.first()
    elif 'profile_id' in kwargs:
        profile=ProfileRepo(request=request).profile(*args, **kwargs)
        member=profile.member_set.first()
    else:
        profile=ProfileRepo(request=request).me
        member=profile.member_set.first()
    
    if member is not None:
        context['member']=member
        context['member_s']=json.dumps(MemberSerializer(member).data)
        channels=[]
        context['channels']=channels
    return context


class HomeViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        channels=ChannelRepo(request=request).list(*args, **kwargs)
        context['channels']=channels

        
        # events=EventRepo(request=request).list(for_home=True,*args, **kwargs)
        # context['events']=events

        
        return render(request,TEMPLATE_ROOT+"index.html",context)


class MessageViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        message=MessageRepo(request=request).message(*args, **kwargs)
        context['message']=message
        return render(request,TEMPLATE_ROOT+"message.html",context)


class SendSMSView(View):
    def post(self,request,*args, **kwargs):
        return SendSMSApi().post(request=request)
    
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+"send-sms.html",context)
    

class ChannelViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        channel=ChannelRepo(request=request).channel(*args, **kwargs)
        context['channel']=channel
        messages=MessageRepo(request=request).list(channel_id=channel.id,*args, **kwargs).order_by("-id")
        context['messages']=messages
        context.update(get_member_context(request=request))
        members=channel.member_set.all()
        context['members']=members
        context['members_s']=json.dumps(MemberSerializer(members,many=True).data)
        return render(request,TEMPLATE_ROOT+"channel.html",context)


class MemberView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        member=MemberRepo(request=request).member(*args, **kwargs)
        context['member']=member
        return render(request,TEMPLATE_ROOT+"member.html",context)

