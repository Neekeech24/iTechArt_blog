import factory
import unittest
from django.test import TestCase, Client

from blog_app.models import Article
from blog_app.tasks import last_added_comments
from profile_app.tests import UserFactory


class ArticleFactory(factory.django.DjangoModelFactory):
    author = factory.SubFactory(UserFactory)
    theme = factory.Sequence(lambda n: 'Theme-%01d' % n)
    text = 'Lorem Ipsum dolor'

    class Meta:
        model = Article
        django_get_or_create = ('theme',)


class ArticleCreateTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = UserFactory.create()

    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)

    def test_non_logged_user(self):
        self.client.logout()
        response = self.client.post('/create_article', {'theme': 'Тема', 'text': 'Текст', 'author': self.client})
        self.assertRedirects(response, '/accounts/login/?next=/create_article')

    def test_empty_form(self):
        response = self.client.post('/create_article', {})
        expected_errors = {
            'theme': ['Обязательное поле.'],
            'text': ['Обязательное поле.'],
            'author': ['Обязательное поле.']
        }
        received_errors = dict(zip(response.context['form'].errors.keys(), response.context['form'].errors.values()))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(expected_errors, received_errors)

    def test_non_unique_theme(self):
        article = ArticleFactory.create(theme='Theme')
        response = self.client.post('/create_article', {'theme': 'Theme',
                                                        'text': 'Text',
                                                        'author': self.user.id})
        expected_errors = {
            'theme': ['Статья с указанной темой уже существует.']
        }
        received_errors = dict(zip(response.context['form'].errors.keys(), response.context['form'].errors.values()))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(expected_errors, received_errors)

    def test_correct_article_form(self):
        response = self.client.post('/create_article', {'theme': 'Theme',
                                                        'text': 'Text',
                                                        'author': self.user.id})
        self.assertRedirects(response, '/article/1')


class MainPageTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.articles = ArticleFactory.create_batch(10)
        cls.user = UserFactory.create()

    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)

    def test_main_page(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(10, len(response.context['object_list']))

    def test_main_page_filter(self):
        response = self.client.get('', {'search-request': 'Theme-2'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(response.context['object_list']))