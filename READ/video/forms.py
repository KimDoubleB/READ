from django import forms
from .models import Video

class RegisterForm(forms.Form):
    name = forms.CharField(
        error_messages={
            'required':'비디오 제목을 입력해주세요.'
        },
        max_length=64,
        label='비디오 제목'
    )
    playlist = forms.IntegerField(
        error_messages={
            'required':'비디오 게수를 입력해주세요.'
        },
        label='비디오 개수'
    )
    description = forms.CharField(
        error_messages={
            'required':'비디오 설명을 입력해주세요.'
        },
        label='비디오 설명'
    )
    
    file = forms.FileField(
        error_messages={
            'required':'비디오 파일을 업로드해주세요.'
        },
        label='비디오 파일'
    )
