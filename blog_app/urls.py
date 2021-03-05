from django.urls import path
from .views import main_page, article_detail, create_article

urlpatterns = [
    path('', main_page, name='main_page'),
    path('article/<article_id>', article_detail, name='article_detail'),
    path('create_article', create_article, name='create_article'),
]