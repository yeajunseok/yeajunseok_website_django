from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post, Category
from django.utils import timezone
from django.contrib.auth.models import User


def create_category(name='life', description=''):
    category, is_created = Category.objects.get_or_create( # 있으면 get가져와서 categorty에 저장하고, 없으면 create해서 categorty에 저장, is_created는 T,F 저장.
        name = name,
        description = description
    )
    return category

def create_post(title, content, author, category=None):
    blog_post = Post.objects.create(
        title=title,
        content=content,
        created=timezone.now(),
        author=author,
        category=category,
    )
    return blog_post


# Create your tests here.
class TestModel(TestCase):
    def setUp(self):
        self.client = Client() # 이전에는 직접 브라우저로 확인했는데, 이 Client가 대신 해준다.
        self.author_000 = User.objects.create(username='smith', password='nopassword')

    def test_category(self):
        category = create_category()

        post_000 = create_post(
            title='The first post',
            content='Hello World. We are the world',
            author=self.author_000,
            category=category
        )
        self.assertEqual(category.post_set.count(),1) # category.post_set : category에 연결된 post들의 수를 알수 있다.

    def test_post(self):
        category = create_category(

        )
        post_000 = create_post(
            title='The first post',
            content='Hello World. We are the world',
            author=self.author_000,
            category=category
        )

class TestView(TestCase):
    def setUp(self):
        self.client = Client() # 이전에는 직접 브라우저로 확인했는데, 이 Client가 대신 해준다.
        self.author_000 = User.objects.create(username='smith', password='nopassword')

    def check_navbar(self, soup):
        navbar = soup.find('div', id='navbar')
        self.assertIn('Blog', navbar.text)
        self.assertIn('About me', navbar.text)

    def test_post_list_no_post(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.title
        self.assertEqual(title.text, 'Blog')

        self.check_navbar(soup)

        self.assertEqual(Post.objects.count(), 0) # .count는 몇개있는지 알아오기, 그리고 test에서는 실제DB와 상관없다, 걍 0이 맞다.
        # Post.object.all() : 전부 가져오기, # Post.object.get() : 하나만 가져오기
        self.assertIn('아직 게시물이 없습니다.', soup.body.text)

    def test_post_list_with_post(self):
        post_000 = create_post(
            title = 'The first post',
            content = 'Hellow World. We are the wordl',
            author = self.author_000,
        )

        post_001 = create_post(
            title='The second post',
            content='Second sedond 두번쨰',
            author=self.author_000,
            category=create_category(name='정치/사회')
        )

        self.assertGreater(Post.objects.count(), 0) # 0보다 크니?

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        body = soup.body
        self.assertNotIn('아직 게시물이 없습니다.', body.text)
        self.assertIn(post_000.title, body.text)

        post_000_read_more_btn = body.find('a', id='read-more-post-{}'.format(post_000.pk))
        # print(post_000_read_more_btn.text), # print(post_000_read_more_btn['href'])
        self.assertEqual(post_000_read_more_btn['href'], post_000.get_absolute_url())

        # category card 에서
        category_card = body.find('div', id='category-card')
        self.assertIn('미분류 (1)', category_card.text) # 미분류(1) 있어야 함
        self.assertIn('정치/사회 (1)', category_card.text) # 정치/사회(1) 있어야 함

        # main_div 에는
        main_div = body.find('div', id='main_div')
        self.assertIn('정치/사회', main_div.text) # '정치/사회' 있어야 함
        self.assertIn('미분류', main_div.text) # '미분류' 있어야 함



    def test_post_detail(self):
        post_000 = create_post(
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