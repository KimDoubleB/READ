from django.db import models

class User_Image(models.Model):
    cover = models.ImageField(upload_to='images/')
