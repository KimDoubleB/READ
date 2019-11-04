from django.shortcuts import render, redirect
from .models import User_Image
from .forms import ImageForm
from django.views.decorators.csrf import csrf_exempt

from user.models import READ_User
from video.models import Video
from .models import User_Image
from django.core.files.storage import default_storage

@csrf_exempt
def image_view(request):
    template ='image.html'
    form = ImageForm(request.POST, request.FILES)
    if form.is_valid():
        # save image file        
        image = request.FILES['cover']
        image_file = default_storage.save('images/' + image.name, image)

        # data processing
        video = Video.objects.get(pk = form.data.get('video'))
        user = READ_User.objects.get(username = form.data.get('user'))
        currentTime = int(float(form.data.get('currentTime')) / 10)
        path = 'images/' + form.data.get('path')
        
        # save model
        user_img = User_Image(
            user = user,
            video = video,
            currentTime = currentTime,
            path = path,
            reaction = "1" # Temporary data (TODO: deep learning)
        )
        user_img.save()

    else:
        print(form)
        form = ImageForm()

    context = {
        'form' : form,
    }
    return render(request, template, context)
