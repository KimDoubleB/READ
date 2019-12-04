from django.shortcuts import render, redirect
from .models import User_Image
from .forms import ImageForm
from django.views.decorators.csrf import csrf_exempt

from user.models import READ_User
from video.models import Video
from .models import User_Image

from .face_analyzer import analyze_image
from threading import Thread

@csrf_exempt
def image_view(request):
    template ='image.html'
    form = ImageForm(request.POST, request.FILES)
    if form.is_valid():
      # get value of form
      image = request.FILES['cover']
      video = Video.objects.get(pk = form.data.get('video'))
      user = READ_User.objects.get(username = form.data.get('user'))
      currentTime = int(float(form.data.get('currentTime')) / 10)
      path = 'images/' + form.data.get('path')
      
      thread_analyze = Thread(target = analyze_image, args=(user, video, currentTime, path, image, ))
      thread_analyze.start()
    else:
        print(form)
        form = ImageForm()

    context = {
        'form' : form,
    }
    return render(request, template, context)

def result(request):
    # pass session data to template.
    return render(request, 'analyze.html')
