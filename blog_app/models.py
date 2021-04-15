from profile_app.models import UserModel
from django.db import models



# Create your models here.



class Article(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='Автор')
    theme = models.CharField(max_length=128, verbose_name='Заголовок', unique=True)
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.theme

    def get_comment_count(self):
        return self.comment_count
    get_comment_count.short_description = 'Кол-во комментариев'

    def get_rating_count(self):
        return self.rating_count
    get_rating_count.short_description = 'Рейтинг'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-pub_date', 'theme']


class Comment(models.Model):
    auth_user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='Автор', blank=True, null=True)
    anon_user = models.CharField(max_length=40, verbose_name='Session ID', blank=True, null=True)
    username = models.CharField(max_length=40)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comment')
    body = models.CharField(max_length=255, verbose_name='Комментарий')
    pub_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.article.theme

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']


class Rating(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    anon_user = models.CharField(max_length=40, verbose_name='Session ID', blank=True, null=True)
    auth_user = models.ForeignKey(UserModel, on_delete=models.CASCADE, blank=True, null=True)