from threading import Thread

from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from user.models import READ_User
from video.models import Video

from .face_analyzer import analyze_image
from .forms import ImageForm
from .models import User_Image


@csrf_exempt
def analyze_view(request):
    template ='image.html'
    form = ImageForm(request.POST, request.FILES)
    if form.is_valid():
        # get value of form
        image = request.FILES['cover']
        video = Video.objects.get(pk = form.data.get('video'))
        user = READ_User.objects.get(user_id = form.data.get('user'))
        currentTime = int(float(form.data.get('currentTime')) / 10) - 1
        if currentTime < 0: currentTime = 0
        path = 'images/' + form.data.get('path')
        duration = form.data.get('duration')
        thread_analyze = Thread(target = analyze_image, args=(user, video, currentTime, path, image, duration, ))
        thread_analyze.start()
    else:
        print(form)
        form = ImageForm()

    context = {
        'form' : form,
    }
    return render(request, template, context)

def result(request):
    user = READ_User.objects.get(user_id = request.session['user'])
    video = Video.objects.get(id = request.session['video'])
    
    if not User_Image.objects.filter(user=user, video=video).exists():
        return redirect('/video/') # go to the video section.
    else:
        present_user = User_Image.objects.get(user=user, video=video)
        user_name = user.name
        video_name = video.name
        # pass session data to template.
        return render(request, 'analyze_result.html', {'user_name' : user_name, 'video_name': video_name, 'reaction' : present_user.reaction})
