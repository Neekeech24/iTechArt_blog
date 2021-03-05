from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    theme = models.CharField(max_length=128, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-pub_date', 'theme']


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    body = models.CharField(max_length=255, verbose_name='Комментарий')
    pub_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']
