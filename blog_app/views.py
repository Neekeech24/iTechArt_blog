from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from .forms import CreateArticleForm, CreateCommentForm
from .models import Article, Rating


# Create your views here.

class MainPageView(ListView):
    model = Article
    paginate_by = 10
    template_name = 'user/main.html'

    def get_queryset(self):
        print(self.request.GET)
        sr = self.request.GET.get('search-request')
        print(sr)
        sort = self.request.GET.get('sort')
        sort_dict = {'new': '-pub_date', 'old': 'pub_date',
                     'rate-desc': '-rating', 'rate-asc': 'rating',
                     'a-asc':'author', 'a-desc':'-author'}
        queryset = Article.objects.all()
        if sr:
            queryset = queryset.filter(Q(theme__icontains=sr) | Q(text__icontains=sr))
        if sort:
            queryset = queryset.order_by(sort_dict[sort])
        print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sr'] = self.request.GET.get('search-request')
        context['sort'] = self.request.GET.get('sort')
        return context



# ARTICLES BLOCK


def article_detail(request, article_id):
    article = get_object_or_404(Article.objects.prefetch_related('comment_set', 'author'), id=article_id)
    return render(request, 'user/article_detail.html',
                  context={'article': article, 'comments': article.comment_set.all()})


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


def update_rating(request, article_id):
    article = get_object_or_404(Article.objects.prefetch_related('rating_set'), id=article_id)
    if request.user.is_authenticated:
        Rating.objects.get_or_create(article=article, auth_user=request.user)
    else:
        request.session.save()
        Rating.objects.get_or_create(article=article, anon_user=request.session.session_key)
    return redirect('article_detail', article_id=article_id)


# COMMENTS BLOCK


def create_comment(request):
    data = request.POST
    article = get_object_or_404(Article.objects.prefetch_related('comment_set'), id=data['article'])
    form_data = {'article': article, 'body': data['body']}
    if request.user.is_authenticated:
        form_data['auth_user'] = request.user
        form_data['username'] = request.user.username
    else:
        request.session.save()
        form_data['anon_user'] = request.session.session_key
    form = CreateCommentForm(data=form_data)
    if form.is_valid():
        comment = form.save()
        return JsonResponse(data=model_to_dict(comment))
    else:
        return JsonResponse(form.errors.as_json(), safe=False)
