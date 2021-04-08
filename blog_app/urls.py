from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import article_detail, update_article,\
    delete_article, update_rating, create_comment,\
    MainPageView, CreateArticleView

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('article/<article_id>', article_detail, name='article_detail'),
    path('create_article', login_required(CreateArticleView.as_view()), name='create_article'),
    path('update_article/<article_id>', update_article, name='update_article'),
    path('delete_article/<article_id>', delete_article, name='delete_article'),
    path('update_rating/<article_id>', update_rating, name='update_rating'),
    path('create_comment', create_comment, name='create_comment')
]