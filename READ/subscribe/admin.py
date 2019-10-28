from django.contrib import admin
from .models import Subscribe

class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', )

admin.site.register(Subscribe, SubscribeAdmin)