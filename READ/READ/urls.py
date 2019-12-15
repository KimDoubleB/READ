"""READ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# TODO: Subdivided into several url files of each app.
from django.contrib import admin
from django.urls import path
from user.views import RegisterView, LoginView, index, logout, login_API, register_API
from video.views import VideoCreate, VideoList, VideoDetail, VideoWatch, VideoFileView, VideoListAPI, VideoDetailAPI
from subscribe.views import SubscribeCreate, SubscribeList, SubscribeListAPI
from analyzer.views import analyze_view, result, new

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', logout),
    path('video/', VideoList.as_view()),
    path('video/create/', VideoCreate.as_view()),
    path('video/<int:pk>/', VideoDetail.as_view()),
    path('video/<int:pk>/watch/', VideoWatch.as_view()),
    path('get_video/<file_name>/', VideoFileView.as_view()),
    path('subscribe/', SubscribeList.as_view()),
    path('subscribe/create/', SubscribeCreate.as_view()),
    path('result/', result),
    path('upload/', analyze_view),
    path('api/login/', login_API),
    path('api/register/', register_API),
    path('api/video/', VideoListAPI.as_view()),
    path('api/video/<int:pk>/', VideoDetailAPI.as_view()),
    path('api/subscribe/', SubscribeListAPI.as_view()),
    path('new/', new),
]
