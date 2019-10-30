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
from user.views import RegisterView, LoginView, index, logout
from video.views import VideoCreate, VideoList, VideoDetail
from subscribe.views import SubscribeCreate, SubscribeList

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', logout),
    path('video/', VideoList.as_view()),    
    path('video/<int:pk>/', VideoDetail.as_view()),
    path('video/create/', VideoCreate.as_view()),
    path('subscribe/', SubscribeList.as_view()),
    path('subscribe/create/', SubscribeCreate.as_view()),

]
