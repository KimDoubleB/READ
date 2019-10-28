from django import forms
from .models import Subscribe
from django.db import transaction
from video.models import Video

class RegisterForm(forms.Form):

    # session에 접근하기 위해 request를 받아와야 한다.
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request


    # 사용자 정보의 경우, session에서 가지고 있기 때문에 따로 넣을 필요가 없다.
    # 물품 정보의 경우, 물품 detail 페이지에서 주문이 이루어지므로 Hidden input으로 따로 정보를 받지 않도록 한다.

    video = forms.IntegerField(
        error_messages={
            'required': '비디오를 입력해주세요.'
        },
        label='비디오', widget=forms.HiddenInput
    )
    
    def clean(self):
        cleaned_data = super().clean()

        # product_detail부분을 통해서 value로 product_id를 받아 왔다.
        # pk값(id - 순서)를 가져온 것. --> 해당 form은 view를 보면 알겠지만 detail를 통해 접근할 경우, product 값은 무조건 가져오게 되어 있다.
        video = cleaned_data.get('video')
        
        if not video:
            self.add_error('video', '값이 없습니다.')