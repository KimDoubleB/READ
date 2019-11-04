from django.contrib import admin
from .models import User_Image

class ImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'currentTime', 'path', )


admin.site.register(User_Image, ImageAdmin)
