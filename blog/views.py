from django.shortcuts import render
from .models import Post
# Create your views here.

def index(request):
    posts = Post.objects.all()
    return render(
        request,
        'blog/index.html',
        {
            # 'posts'랑 'a_plus_b' 가 templates/blog/index.html 파일의 {{ '제목' }} 으로 들어간다.
            'posts': posts,
            'a_plus_b': 1+3,
        }
    )