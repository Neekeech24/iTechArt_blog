from django.urls import path, include
from .views import main_page, article_detail, create_article,\
    profile_detail, delete_profile, user_profile, registration,\
    update_article, delete_article
from django.contrib.auth import urls

urlpatterns = [
    path('', main_page, name='main_page'),
    path('article/<article_id>', article_detail, name='article_detail'),
    path('create_article', create_article, name='create_article'),
    path('update_article/<article_id>', update_article, name='update_article'),
    path('delete_article/<article_id>', delete_article, name='delete_article'),
    path('accounts/', include(urls)),
    path('accounts/profile/', user_profile, name='user_profile'),
    path('accounts/profile/<user_id>', profile_detail, name='profile_detail'),
    path('delete_profile', delete_profile, name='delete_profile'),
    path('registration', registration, name='registration')
]