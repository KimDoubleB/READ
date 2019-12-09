import os
import random
import string
from wsgiref.util import FileWrapper

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from django.views.generic.base import HttpResponse, HttpResponseRedirect, View
from django.views.generic.edit import FormView
from rest_framework import generics, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST)

from analyzer.models import User_Image
from subscribe.forms import RegisterForm as SubscribeForm
from subscribe.models import Subscribe
from user.level import admin_required
from user.models import READ_User

from .forms import RegisterForm
from .models import Video
from .serializers import VideoSerializer


@method_decorator(admin_required, name='dispatch')
class VideoCreate(View):
    template_name = 'register_video.html'
    def get(self, request):

        form = RegisterForm()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        # pass filled out HTML-Form from View to NewVideoForm()
        form = RegisterForm(request.POST, request.FILES)
    
        print(form)
        print(request.POST)
        print(request.FILES)

        if form.is_valid():
            # check clean
            name = form.cleaned_data['name']
            playlist = form.cleaned_data['playlist']
            description = form.cleaned_data['description']
            file = form.cleaned_data['file']
            if not (name and playlist and description and file):
                self.add_error('file', '값이 없는 항목이 있습니다.')

            # file uploading
            random_char = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            path = random_char+file.name
            addr = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"\media"
            fs = FileSystemStorage(location = addr)
            filename = fs.save(path, file)
            file_url = fs.url(filename)

            # add data to Video DB
            video = Video(
                name = form.data.get('name'),
                playlist = int(form.data.get('playlist')),
                description = form.data.get('description'),
                path = path
            )

            video.save()
            return HttpResponseRedirect('/video/')
        else:
            return HttpResponse('Your form is not valid. Go back and try again.')

class VideoList(ListView):
    model = Video
    template_name = 'video.html'
    context_object_name = 'video_list'
    
    def get_context_data(self,**kwargs):
        context = super(VideoList, self).get_context_data(**kwargs)
        context['user'] = READ_User.objects.get(username=self.request.session.get('user'))
        return context

    def get(self, request):
        if 'video' in request.session:
            del(request.session['video'])
        return super(VideoList, self).get(request)

# Login required
class VideoDetail(DetailView):
    template_name = 'video_detail.html'
    queryset = Video.objects.all()
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session['video'] = context['video'].pk
        user = READ_User.objects.get(username=self.request.session.get('user'))
        subs = Subscribe.objects.filter(user = user)
        context['visible'] = 1

        for sub in subs:
            if sub.video == context['video']:
                context['visible'] = 0
                break

        context['form'] = SubscribeForm(self.request)
        return context

class VideoWatch(View):
    template_name = 'video_watch.html'

    def get(self, request, pk):
        #fetch video from DB by ID
        video = Video.objects.get(id=pk)
        username = self.request.session.get('user')
        user = READ_User.objects.get(username=username)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        video.path = '/./get_video/'+video.path

        if not User_Image.objects.filter(user=user, video=video).exists():
          user_reaction = None
        else:
          user_reaction = User_Image.objects.get(user=user, video=video)

        context = {'user':username, 'video':video, 'user_reaction':user_reaction}

        return render(request, self.template_name, context)


class VideoFileView(View):
    def get(self, request, file_name):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file = FileWrapper(open(BASE_DIR+'/media/'+file_name,'rb'))
        response = HttpResponse(file, content_type='video/mp4')
        response['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
        return response


@permission_classes((IsAuthenticated,))
class VideoListAPI(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = VideoSerializer

    def get_queryset(self):
        return Video.objects.all().order_by('id')

    '''
    게시물 리스트 조회
    /api/video/
    '''
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    '''
    게시물 생성
    /api/video/
    '''
    def post(self, request, format=None):
        serializer = VideoSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response({'error': 'Please provide name and playlist and description'}, 
                        status=HTTP_400_BAD_REQUEST)

@permission_classes((IsAuthenticated,))
class VideoDetailAPI(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = VideoSerializer

    def get_queryset(self):
        return Video.objects.all().order_by('id')
    
    '''
    특정 게시물 조회
    /api/video/{pk}/
    '''
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    '''
    특정 게시물 수정
    /api/video/{pk}/
    '''
    def put(self, request, pk, format=None):
        video = self.get_object()
        serializer = VideoSerializer(video, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response({'error': '올바르지 않은 값이 입력되었습니다.'}, 
                        status=HTTP_400_BAD_REQUEST)
    
    '''
    특정 게시물 삭제
    /api/video/{pk}/
    '''
    def delete(self, request, pk, format=None):
        video = self.get_object()
        video.delete()
        return Response(status = HTTP_200_OK)
