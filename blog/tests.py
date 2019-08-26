from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post
from django.utils import timezone
from django.contrib.auth.models import User


# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client = Client() # 이전에는 직접 브라우저로 확인했는데, 이 Client가 대신 해준다.
        self.author_000 = User.objects.create(username='smith', password='nopassword')
    def test_post_list(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.title
        self.assertEqual(title.text, 'Blog')

        navbar = soup.find('div', id='navbar')
        self.assertIn('Blog', navbar.text)
        self.assertIn('About me', navbar.text)

        self.assertEqual(Post.objects.count(), 0) # .count는 몇개있는지 알아오기, 그리고 test에서는 실제DB와 상관없다, 걍 0이 맞다.
        # Post.object.all() : 전부 가져오기
        # Post.object.get() : 하나만 가져오기
        self.assertIn('아직 게시물이 없습니다.', soup.body.text)

        post_000 = Post.objects.create(
            title = 'The first post',
            content = 'Hello World. We are the world',
            created = timezone.now(),
            author = self.author_000,
        )

        self.assertGreater(Post.objects.count(), 0)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        body = soup.body
        self.assertNotIn('아직 게시물이 없습니다.', body.text)
        self.assertIn(post_000.title, body.text)