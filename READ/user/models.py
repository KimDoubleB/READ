from django.db import models

class READ_User(models.Model):
    username = models.CharField(max_length=128, verbose_name="아이디")
    password = models.CharField(max_length=128, verbose_name="비밀번호")
    token = models.CharField(max_length=128)
    register_date = models.DateTimeField(auto_now_add=True, verbose_name="등록날짜")

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user' # db 테이블 이름 명명
        verbose_name = '사용자' # admin 상에서 관리하기 위한 테이블 이름 명명
        verbose_name_plural = '사용자' # 위와 동일, 복수형시 사용