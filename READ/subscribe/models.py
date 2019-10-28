from django.db import models

class Subscribe(models.Model):
    user = models.ForeignKey('user.READ_User', on_delete=models.CASCADE, verbose_name="사용자")
    video = models.ForeignKey('video.Video', on_delete=models.CASCADE, verbose_name="비디오")
    register_date = models.DateTimeField(auto_now_add=True, verbose_name="등록날짜")


    def __str__(self):
        return str(self.user) + ' ' + str(self.video)


    class Meta:
        db_table = 'Subscribe'
        verbose_name = '구독'
        verbose_name_plural = '구독'