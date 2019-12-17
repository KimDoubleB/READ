from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views.generic.edit import FormView
from rest_framework import generics, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST)

from user.models import READ_User
from video.models import Video

from .forms import RegisterForm
from .models import Subscribe
from .serializers import SubscribeSerializer


class SubscribeList(ListView):
    template_name = 'subscribe.html'
    context_object_name = 'subscribe_list'

    def get_queryset(self, **kwargs):
        queryset = Subscribe.objects.filter(user__user_id = self.request.session.get('user'))
        return queryset
    
    def get(self, request):
        if 'video' in request.session:
            del(request.session['video'])
        return super(SubscribeList, self).get(request)


class SubscribeCreate(FormView):
    form_class = RegisterForm 
    success_url = '/subscribe/'

    def form_valid(self, form):
        video = Video.objects.get(pk=form.data.get('video'))

        subs = Subscribe(
            video = video,
            user = READ_User.objects.get(user_id=self.request.session.get('user'))
        )
        subs.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return redirect('/video/' + str(form.data.get('video')))

    def get_form_kwargs(self, **kwargs):
        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            'request':self.request
        })
        return kw

@permission_classes((IsAuthenticated,))
class SubscribeListAPI(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        return Subscribe.objects.all()

    '''
    구독 리스트 조회
    /api/subscribe/
    '''
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    '''
    게시물 생성
    /api/subscribe/
    '''
    def post(self, request, format=None):
        # user_id과 video name을 받는다고 가정
        video = Video.objects.get(pk = request.data.get('video'))
        user = READ_User.objects.get(pk = request.data.get('user'))
        print(user)
        print(video)
        subs = Subscribe(
            video = video,
            user = user
        )
        subs.save()
        return Response(subs, status=HTTP_201_CREATED)

        return Response({'error': '알맞은 ID 또는 Video 이름을 입력해주십시오'}, 
            status=HTTP_400_BAD_REQUEST)
