from django import forms
from .models import User_Image

class ImageForm(forms.Form):
    user = forms.CharField()
    video = forms.IntegerField()
    currentTime = forms.CharField()
    path = forms.CharField()
    cover = forms.ImageField()
