from django.db import models

class User_Image(models.Model):
    user = models.ForeignKey('user.READ_User', on_delete=models.CASCADE, verbose_name="사용자")
    video = models.ForeignKey('video.Video', on_delete=models.CASCADE, verbose_name="비디오")
    currentTime = models.CharField(max_length=256)
    path = models.CharField(max_length=256)
    reaction = models.TextField()

    
    def __str__(self):
        return str(self.user) + str(self.video) + str(self.currentTime)
