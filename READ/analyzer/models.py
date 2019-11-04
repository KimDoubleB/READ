from django.db import models

class User_Image(models.Model):
    name = models.CharField(max_length=512)
    cover = models.ImageField(upload_to='images/')
    
    def __str__(self):
        return str(self.cover)
