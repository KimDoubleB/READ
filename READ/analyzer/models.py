from django.db import models

class User_Image(models.Model):
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return str(self.cover)

class Reaction(models.Model):
    user = models.ForeignKey('user.READ_User', on_delete=models.CASCADE, verbose_name="사용자")
    video = models.ForeignKey('video.Video', on_delete=models.CASCADE, verbose_name="비디오")
    reaction = models.CharField(max_length=512)
    register_date = models.DateTimeField(auto_now_add=True, verbose_name="등록날짜")

    def __str__(self):
        return str(self.user) + ' ' + str(self.video)