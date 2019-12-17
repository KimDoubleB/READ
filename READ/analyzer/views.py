import json
from threading import Thread

import numpy as np
import pandas as pd
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView

from user.level import admin_required
from user.models import READ_User
from video.models import Video

from .face_analyzer import analyze_image
from .forms import ImageForm
from .models import User_Image


@csrf_exempt
def analyze_view(request):
    template ='image.html'
    form = ImageForm(request.POST, request.FILES)
    if form.is_valid():
        # get value of form
        image = request.FILES['cover']
        video = Video.objects.get(pk = form.data.get('video'))
        user = READ_User.objects.get(user_id = form.data.get('user'))
        currentTime = int(float(form.data.get('currentTime')) / 10) - 1
        if currentTime < 0: currentTime = 0
        path = 'images/' + form.data.get('path')
        duration = form.data.get('duration')
        thread_analyze = Thread(target = analyze_image, args=(user, video, currentTime, path, image, duration, ))
        thread_analyze.start()
    else:
        print(form)
        form = ImageForm()

    context = {
        'form' : form,
    }
    return render(request, template, context)

def result(request):
    if not('user' in request.session) or not('video' in request.session):
        return redirect('/') # go to the home.
    user = READ_User.objects.get(user_id = request.session['user'])
    video = Video.objects.get(id = request.session['video'])
    
    if not User_Image.objects.filter(user=user, video=video).exists():
        return redirect('/video/') # go to the video section.
    else:
        present_user = User_Image.objects.get(user=user, video=video)
        user_name = user.name
        video_name = video.name
        # pass session data to template.
        return render(request, 'analyze_result.html', {'user_name' : user_name, 'video_name': video_name, 'reaction' : present_user.reaction})

@method_decorator(admin_required, name='dispatch')
class DashboardView(ListView):
    template_name = 'dashboard.html'
    context_object_name = 'user_list'
    model = READ_User
    
    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context.update({
            'video_list': Video.objects.order_by('name')
        })
        return context

    def get_queryset(self):
        return READ_User.objects.order_by('name')

@method_decorator(admin_required, name='dispatch')
class DashboardVideoView(DetailView):
    template_name = 'dashboard_video.html'
    queryset = Video.objects.all()
    context_object_name = 'video'
    def get_context_data(self, **kwargs):
        context = super(DashboardVideoView, self).get_context_data(**kwargs)
        analyzer_objects = User_Image.objects.filter(video = context['video'])
        reactions = None
        views = len(analyzer_objects) # length of users
        
        # reaction data convert to dataframe
        reaction_df = pd.DataFrame([], columns=range(json.loads(analyzer_objects[0].reaction)['duration']))
        duration = reaction_df.columns
        for i, ao in enumerate(analyzer_objects):
            reaction = np.array(json.loads(ao.reaction)['time'])
            reaction_df.loc[i] = reaction
        
        # fit to graph data
        graph_data = pd.DataFrame([], columns=[0,1,2,3])
        for time in reaction_df.columns:
            data = reaction_df.iloc[:, time].value_counts()
            graph_data = graph_data.append(data, ignore_index=True)
    
        # graph data package
        graph_data = graph_data.fillna(0).T
        graph_pie_data = graph_data.sum(axis=1)
        
        context.update({
            'duration': list(duration),
            'graph': graph_data.values.tolist(),
            'graph_pie': graph_pie_data.values.tolist(),
            'user_list': READ_User.objects.order_by('name'),
            'video_list': Video.objects.order_by('name')
        })   
        return context

@method_decorator(admin_required, name='dispatch')
class DashboardUserView(DetailView):
    template_name = 'dashboard_user.html'
    queryset = READ_User.objects.all()
    context_object_name = 'user'
    def get_context_data(self, **kwargs):
        context = super(DashboardUserView, self).get_context_data(**kwargs)
        analyzer_objects = User_Image.objects.filter(user=context['user'])
        vids = []
        for obj in analyzer_objects:
            json_data = json.loads(obj.reaction)
            
            # get data from json
            duration = json_data['duration']
            reaction = np.array(json_data['time'])
            
            # calculate ratio
            ratio = np.count_nonzero(reaction == 0) / duration * 100
            vids.append([obj.video.name, ratio])
            
        context.update({
            'vids': vids,
            'user_list': READ_User.objects.order_by('name'),
            'video_list': Video.objects.order_by('name')
        })
        return context


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = READ_User.objects.get(user_id=self.request.session.get('user'))
    #     subs = Subscribe.objects.filter(user = user)
    #     context['visible'] = 1

    #     for sub in subs:
    #         if sub.video == context['video']:
    #             context['visible'] = 0
    #             break

    #     context['form'] = SubscribeForm(self.request)
    #     return context
