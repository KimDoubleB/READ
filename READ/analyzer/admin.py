from django.contrib import admin
from .models import User_Image, Reaction

class ImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'cover', )

class ReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'video',)

admin.site.register(User_Image, ImageAdmin)
admin.site.register(Reaction, ReactionAdmin)