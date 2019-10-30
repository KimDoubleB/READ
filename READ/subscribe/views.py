from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import ListView
from .forms import RegisterForm
from .models import Subscribe
from video.models import Video
from user.models import READ_User


class SubscribeList(ListView):
    template_name = 'subscribe.html'
    context_object_name = 'subscribe_list'

    def get_queryset(self, **kwargs):
        queryset = Subscribe.objects.filter(user__username = self.request.session.get('user'))
        return queryset


class SubscribeCreate(FormView):
    form_class = RegisterForm 
    success_url = '/subscribe/'

    def form_valid(self, form):
        video = Video.objects.get(pk=form.data.get('video'))

        subs = Subscribe(
            video = video,
            user = READ_User.objects.get(username=self.request.session.get('user'))
        )
        subs.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return redirect('/video/' + str(form.data.get('video')))

    def get_form_kwargs(self, **kwargs):
        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            'request':self.request
        })
        return kw