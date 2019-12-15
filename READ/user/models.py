from django.db import models

class READ_User(models.Model):
    user_id = models.CharField(max_length=128, verbose_name="아이디")
    password = models.CharField(max_length=128, verbose_name="비밀번호")
    name = models.CharField(max_length=15, verbose_name="이름")
    gender = models.CharField(max_length=1, verbose_name="성별",
                              choices=(
                                  ('M', 'Male'),
                                  ('F', 'Female')                                  
                              ))
    level = models.CharField(max_length=8, default='user',
                             choices=(
                                 ('admin', 'admin'),
                                 ('user', 'user')
                             ))
    job = models.CharField(max_length=30, verbose_name="직업")
    place = models.CharField(max_length=30, verbose_name="학교/회사")
    age = models.IntegerField(verbose_name="나이")

    token = models.CharField(max_length=128)
    register_date = models.DateTimeField(auto_now_add=True, verbose_name="등록날짜")

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = 'user' # db 테이블 이름 명명
        verbose_name = '사용자' # admin 상에서 관리하기 위한 테이블 이름 명명
        verbose_name_plural = '사용자' # 위와 동일, 복수형시 사용