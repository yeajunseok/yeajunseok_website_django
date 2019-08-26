from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post
from django.utils import timezone
from django.contrib.auth.models import User


def creat_post(title, content, author):
    blog_post = Post.objects.create(
        title=title,
        content=content,
        created=timezone.now(),
        author=author,
    )
    return blog_post

# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client = Client() # 이전에는 직접 브라우저로 확인했는데, 이 Client가 대신 해준다.
        self.author_000 = User.objects.create(username='smith', password='nopassword')

    def check_navbar(self, soup):
        navbar = soup.find('div', id='navbar')
        self.assertIn('Blog', navbar.text)
        self.assertIn('About me', navbar.text)

    def test_post_list(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.title
        self.assertEqual(title.text, 'Blog')

        self.check_navbar(soup)

        self.assertEqual(Post.objects.count(), 0) # .count는 몇개있는지 알아오기, 그리고 test에서는 실제DB와 상관없다, 걍 0이 맞다.
        # Post.object.all() : 전부 가져오기
        # Post.object.get() : 하나만 가져오기
        self.assertIn('아직 게시물이 없습니다.', soup.body.text)

        post_000 = creat_post(
            title = 'The first post',
            content = 'Hellow World. We are the wordl',
            author = self.author_000,
        )

        self.assertGreater(Post.objects.count(), 0)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        body = soup.body
        self.assertNotIn('아직 게시물이 없습니다.', body.text)
        self.assertIn(post_000.title, body.text)

        post_000_read_more_btn = body.find('a', id='read-more-post-{}'.format(post_000.pk))
        # print(post_000_read_more_btn.text)
        # print(post_000_read_more_btn['href'])
        self.assertEqual(post_000_read_more_btn['href'], post_000.get_absolute_url())


    def test_post_detail(self):
        post_000 = creat_post(
            title = 'The first post',
            content = 'Hellow World. We are the wordl',
            author = self.author_000,
        )

        self.assertGreater(Post.objects.count(), 0)
        post_000_url = post_000.get_absolute_url()
        self.assertEqual(post_000_url, '/blog/{}/'.format(post_000.pk))

        response = self.client.get(post_000_url)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.title
        self.assertEqual(title.text, '{}-Blog'.format(post_000.title))
        self.check_navbar(soup)

        body = soup.body
        main_div = body.find('div', id='main_div')
        self.assertIn(post_000.title, main_div.text)
        self.assertIn(post_000.author.username, main_div.text)

        self.assertIn(post_000.content, main_div.text)