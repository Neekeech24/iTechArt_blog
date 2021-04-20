import datetime

from django.db.models import Prefetch, OuterRef
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from iTechArt import settings
from .models import Article, Comment


@shared_task
def last_added_comments():
    articles = Article.objects.select_related('author').filter(comment__pub_date__gte=timezone.now() - datetime.timedelta(days=1))\
        .prefetch_related(Prefetch('comment', queryset=Comment.objects.filter(pub_date__gte=timezone.now() - datetime.timedelta(days=1)),
                                   to_attr='last_comments'))
    user_list = set([article.author for article in articles])
    for user in user_list:
        message = f"Hello, {user.username}! \n"
        user_articles = {article for article in articles if article.author_id == user.id}
        for article in user_articles:
            article_comments = [comment for comment in article.last_comments]
            for comment in article_comments:
                message += f"Your article {comment.article.theme} received comment {comment.body} from {comment.username}. \n"
        send_mail('Last comments', message, settings.EMAIL_HOST_USER, [user.email, ])





