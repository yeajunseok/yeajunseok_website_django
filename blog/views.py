from django.shortcuts import render
from .models import Post
from django.views.generic import ListView
# Create your views here.

class PostList(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.order_by('-created') # 나중에 작성한 post가 위로 오게

#def index(request):
#    posts = Post.objects.all() # 어떤 모델을 불러와서 이것을 어떤 탬플릿에 담아서 어떤 딕셔너리에 담아서 템플릿에 넘겨주는 것이 여기서 이뤄짐
#    return render(
#        request,
#        'blog/index.html',
#        {
#            # 'posts'랑 'a_plus_b' 가 templates/blog/index.html 파일의 {{ '제목' }} 으로 들어간다.
#            'posts': posts,
#            'a_plus_b': 1+3,
#        }
#    )