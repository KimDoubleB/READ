from django.shortcuts import render, redirect
from .models import User_Image
from .forms import ImageForm
from django.views.decorators.csrf import csrf_exempt

from user.models import READ_User
from video.models import Video
from .models import User_Image

@csrf_exempt
def image_view(request):
    template ='image.html'
    form = ImageForm(request.POST, request.FILES)
    if form.is_valid():
        print(form.data.get('cover'))
        print(request.FILES)
        
        video = Video.objects.get(pk = form.data.get('video'))
        user = READ_User.objects.get(username = form.data.get('user'))

        user_img = User_Image(
            user = user,
            video = video,
            currentTime = form.data.get('currentTime'),
            path = form.data.get('path'),
            reaction = form.data.get('reaction')
        )
        user_img.save()

    else:
        print(form)
        form = ImageForm()

    context = {
        'form' : form,
    }
    return render(request, template, context)
