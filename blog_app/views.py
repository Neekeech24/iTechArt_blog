from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from .forms import CreateArticleForm, CreateCommentForm
from .models import Article


# Create your views here.

class MainPageView(ListView):
    model = Article
    paginate_by = 10
    template_name = 'user/main.html'

    def get_queryset(self):
        sr = self.request.GET.get('search-request')
        sort = self.request.GET.get('sort')
        sort_dict = {'new': '-pub_date', 'old': 'pub_date',
                     'rate-desc': '-rating', 'rate-asc': 'rating'}
        if sr:
            queryset = Article.objects.filter(Q(theme__icontains=sr) | Q(text__icontains=sr))
        else:
            queryset = Article.objects.all()
        if sort:
            queryset = queryset.order_by(sort_dict[sort])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sr'] = self.request.GET.get('search-request')
        context['sort'] = self.request.GET.get('sort')
        return context


# ARTICLES BLOCK


def article_detail(request, article_id):
    article = get_object_or_404(Article.objects.prefetch_related('comment_set', 'author'), id=article_id)
    if request.method == 'POST':
        if request.POST.get('body'):
            create_comment(request, data=request.POST)
        elif request.POST.get('rating') == True:
            update_rating(request, article_id)
    return render(request, 'user/article_detail.html', context={'article': article})


@login_required
def create_article(request):
    form = CreateArticleForm(initial={'author': request.user})
    errors = None
    if request.method == 'POST':
        form = CreateArticleForm(data=request.POST)
        if form.is_valid():
            article = form.save()
            return article_detail(request, article.id)
        elif 'theme' in form.errors:
            errors = form.errors
            form = CreateArticleForm(initial={'author': request.user, 'text': request.POST.get('text')})
        else:
            errors = form.errors
            form = CreateArticleForm()
    return render(request, 'user/create_article.html', context={'form': form, 'errors': errors})


@login_required
def update_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if article.author == request.user:
        form = CreateArticleForm(initial={'theme': article.theme, 'text': article.text, 'author': article.author},
                                 instance=article)
        if request.method == 'POST':
            form = CreateArticleForm(instance=article, data=request.POST)
            if form.is_valid():
                article = form.save()
                return redirect('article_detail', article_id=article.id)
            else:
                form = CreateArticleForm(instance=article)
        return render(request, 'user/create_article.html', context={'form': form})
    else:
        return render(request, '404.html')


@login_required
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if article.author == request.user:
        article.delete()
        return redirect('main_page')
    else:
        return render(request, '404.html')


# def update_rating(request, article_id):
#     key = request.session.session_key
#     article = get_object_or_404(Article.objects.prefetch_related('rating_set'), id=article_id)
    # return HttpResponse()

# COMMENTS BLOCK


@login_required
def create_comment(request, data):
    form = CreateCommentForm(data=data)
    print(form.errors)
    if form.is_valid():
        form.save()
