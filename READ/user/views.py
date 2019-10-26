from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormView

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from .models import READ_User
from .forms import RegisterForm, LoginForm

@csrf_exempt
def index(request):
    # pass session data to template.
    return render(request, 'index.html', {'name' : request.session.get('user') })

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '../login'

    def form_valid(self, form):
        user = User(
            username = form.data.get('username'),
            password = make_password(form.data.get('password'))
        )
        user.save()
        token, _ = Token.objects.get_or_create(user=user)

        # TODO: Duplicated model (user db)
        # combine into one model or use foreign key.
        # Token --> API
        read_user = READ_User(
            username = form.data.get('username'),
            password = make_password(form.data.get('password')),
            token = token
        )
        read_user.save()

        return super().form_valid(form)

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    
    success_url = '/'

    def form_valid  (self, form):
        # session process.
        self.request.session['user'] = form.data.get('username')
        return super().form_valid(form)

def logout(request):
    if 'user' in request.session:
        del(request.session['user'])
    return redirect('/login')