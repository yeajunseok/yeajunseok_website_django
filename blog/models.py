from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30) # CharField는 무조건 길이 조건이 있어야 한다.
    content = models.TextField() # TextField는 길이 조건이 없다.

    created = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=True) #on_delete는 사용자가 퇄퇴했을때 글등이 같이 삭제된다.

    def __str__(self): #post 목록 이름이 어떻게 출력되는지 설정
        return '{} :: {}'.format(self.title, self.author)