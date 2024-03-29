from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=30) # CharField는 무조건 길이 조건이 있어야 한다.
    content = models.TextField() # TextField는 길이 조건이 없다.

    head_image = models.ImageField(upload_to='blog/%Y/%m', blank=True) # blank=True 꼭 채우지 않아도 된다. 그리고 이미지 저장 경로지정은 프로젝트의 settings에서 MEDIA_ROOT에 해준다.

    created = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=True) #on_delete는 사용자가 퇄퇴했을때 글등이 같이 삭제된다.

    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self): #post 목록 이 름이 어떻게 출력되는지 설정
        return '{} :: {}'.format(self.title, self.author)

    def get_absolute_url(self): # admin에서 post추가에 view on site라는 버튼이 추가됨
        return '/blog/{}/'.format(self.pk)

