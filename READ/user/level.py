from django.shortcuts import redirect
from .models import READ_User

def admin_required(function):
    def wrap(request, *args, **kwargs):
        user = request.session.get('user')
        if user is None or not user:
            return redirect('/login')
        
        user = READ_User.objects.get(username=user)
        if user.level != 'admin':
            return redirect('/') # go to the home.
        
        return function(request, *args, **kwargs)
    return wrap
        