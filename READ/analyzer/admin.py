from django.contrib import admin
from .models import User_Image

class ImageAdmin(admin.ModelAdmin):
    list_display = ('cover', )

admin.site.register(User_Image, ImageAdmin)