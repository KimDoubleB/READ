from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND)

from .forms import LoginForm, RegisterForm
from .models import READ_User


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
            username = form.data.get('user_id'),
            password = make_password(form.data.get('password'))
        )
        user.save()
        token, _ = Token.objects.get_or_create(user=user)

        # TODO: Duplicated model (user db)
        # combine into one model or use foreign key.
        # Token --> API
        read_user = READ_User(
            user_id = form.data.get('user_id'),
            password = make_password(form.data.get('password')),
            name = form.data.get('name'),
            gender = form.data.get('gender'),
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
        self.request.session['user'] = form.data.get('user_id')
        return super().form_valid(form)

def logout(request):
    if 'user' in request.session:
        del(request.session['user'])
    return redirect('/login')

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def register_API(request):
    user_id = request.data.get("user_id")
    password = request.data.get("password")
    re_password = request.data.get("re_password")
   
    if user_id is None or password is None or re_password is None:
        return Response({'error': 'Please provide both user_id and password'},
                        status=HTTP_400_BAD_REQUEST)
    if password != re_password:
        return Response({'error': 'Password is not same'},
                        status=HTTP_400_BAD_REQUEST)

    user = User(
        user_id = user_id,
        password = make_password(password)
        )
    user.save()
    token, _ = Token.objects.get_or_create(user=user)

    # Custom model 저장
    read_user = READ_User(
        user_id = user_id,
        password = make_password(password),
        token = token
    )
    read_user.save()
    
    return Response({'Response': 'Permit'},
                  #  {'cover':image},
                    status=HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login_API(request):
    user_id = request.data.get("user_id")
    password = request.data.get("password")
   # image = request.data.get("cover")

    if user_id is None or password is None:
        return Response({'error': 'Please provide both user_id and password'},
                        status=HTTP_400_BAD_REQUEST)
    
    user = authenticate(user_id=user_id, password=password)

    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    
    read_user = READ_User.objects.get(user_id = user_id)
    token = read_user.token
    return Response({'token': token},
                  #  {'cover':image},
                    status=HTTP_200_OK)
