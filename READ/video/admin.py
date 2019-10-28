from django.contrib import admin
from .models import Video

class VideoAdmin(admin.ModelAdmin):
    list_display = ('name', ) 

admin.site.register(Video, VideoAdmin)
