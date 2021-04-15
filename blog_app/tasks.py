import datetime

from django.db.models import Prefetch
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from iTechArt import settings
from .models import Article, Comment


@shared_task
def last_added_comments():
    articles = Article.objects.filter(comment__pub_date__gte=timezone.now() - datetime.timedelta(days=1))\
        .prefetch_related(Prefetch('comment', queryset=Comment.objects.filter(pub_date__gte=timezone.now() - datetime.timedelta(days=1)),
                                   to_attr='last_comments'))
    for article in articles:
        last_comments = [x for x in article.last_comments]
        if last_comments:
            message = 'Hello! \n'
            for comment in last_comments:
                message += f'Your article {comment.article} received new comment "{comment.body}" from {comment.username}. \n'
            send_mail('Last comments to your articles', message, settings.EMAIL_HOST_USER, [article.author.email, ])
