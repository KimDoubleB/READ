from django.db import models

class Video(models.Model):
    name = models.CharField(verbose_name="비디오", max_length=256)
    playlist = models.IntegerField(verbose_name="비디오 개수")
    description = models.TextField(verbose_name="비디오 설명")
    register_date = models.DateTimeField(auto_now_add = True, verbose_name="등록날짜")
    path = models.CharField(max_length=60, null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'video'              # db table name
        verbose_name = '비디오'         # db table name in admin
        verbose_name_plural = '비디오'  # db table name in admin