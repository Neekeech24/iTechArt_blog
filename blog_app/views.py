from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from .models import Article
from .forms import CreateArticleForm


# Create your views here.
def main_page(request):
    return render(request, 'user/main.html', context={'articles': Article.objects.all(), 'user': request.user})


def login(request):
    pass


def logout(request):
    pass


def article_detail(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
        return render(request, 'user/article_detail.html', context={'article': article})
    except ObjectDoesNotExist:
        return render(request, '404.html')


@login_required
def create_article(request):
    form = CreateArticleForm(initial={'author': request.user})
    if request.method == 'POST':
        form = CreateArticleForm(data=request.POST)
        if form.is_valid():
            article = form.save()
            return article_detail(request, article.id)
        else:
            form = CreateArticleForm()
    return render(request, 'user/create_article.html', context={'form': form})
