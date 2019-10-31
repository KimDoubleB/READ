from django.shortcuts import render, redirect
from .models import User_Image
from .forms import ImageForm
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def image_view(request):
    template ='image.html'
    form = ImageForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('/')

    else:
        print(form)
        form = ImageForm()

    context = {
        'form' : form,
    }
    return render(request, template, context)
