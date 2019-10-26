from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

class RegisterForm(forms.Form):
    username = forms.CharField(
        error_messages={
            'required':'아이디을 입력해주세요.'
        },
        max_length=64,
        label='아이디'
    )

    password = forms.CharField(
        error_messages={
            'required':'비밀번호를 입력해주세요.'
        },
        widget=forms.PasswordInput,
        label='비밀번호'
    )

    re_password = forms.CharField(
        error_messages={
            'required':'비밀번호 확인을 입력해주세요.'
        },
        widget=forms.PasswordInput,
        label='비밀번호 확인'
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')

        if password and re_password:
            if password != re_password:
                self.add_error('re_password', '비밀번호가 서로 다릅니다.')
           

class LoginForm(forms.Form):
    username = forms.CharField(
        error_messages={
            'required':'아이디를 입력해주세요.'
        },
        max_length=64,
        label='아이디'
    )

    password = forms.CharField(
        error_messages={
            'required':'이메일을 입력해주세요.'
        },
        widget=forms.PasswordInput,
        label='비밀번호'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                user = User.objects.get(username = username)
                if not check_password(password, user.password):
                    self.add_error('password', '존재하지 않는 이메일이거나 비밀번호가 틀렸습니다.')
            except User.DoesNotExist:
                self.add_error('password', '존재하지 않는 이메일이거나 비밀번호가 틀렸습니다.')
            
