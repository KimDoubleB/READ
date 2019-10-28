import os
import random
import string

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.base import HttpResponse, HttpResponseRedirect, View
from django.views.generic.edit import FormView

from user.models import READ_User

from .forms import RegisterForm
from .models import Video


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
            fs = FileSystemStorage(location = os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            filename = fs.save(path, file)
            file_url = fs.url(filename)
            print(filename, file_url)
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
