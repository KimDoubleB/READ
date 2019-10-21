from django.contrib import admin
from .models import READ_User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', )  # tuple 형태로

admin.site.register(READ_User, UserAdmin)