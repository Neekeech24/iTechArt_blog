from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from .models import Article
from .forms import CreateArticleForm, UpdateUserForm


# Create your views here.
def main_page(request):
    return render(request, 'user/main.html', context={'articles': Article.objects.all(), 'user': request.user})


def article_detail(request, article_id):
    article = get_object_or_404(Article.objects.select_related('author'), id=article_id)
    return render(request, 'user/article_detail.html', context={'article': article})


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


@login_required
def profile_detail(request, user_id):
    user = get_object_or_404(User.objects.prefetch_related('article_set'), id=user_id)
    if request.method == 'POST':
        form = UpdateUserForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'user/profile_detail.html', context={'user': user})


@login_required
def user_profile(request):
    return redirect('profile_detail', user_id=request.user.id)


@login_required
def delete_profile(request):
    user = get_object_or_404(User, id=request.user.id)
    logout(request)
    user.delete()
    return redirect('main_page')


def registration(request):
    if request.method == 'POST':
        if request.POST.get('password') == request.POST.get('password2'):
            try:
                user = User.objects.create(username=request.POST.get('username'))
                user.set_password(request.POST.get('password'))
                user.save()
                new_user = authenticate(username=request.POST.get('username'),
                                        password=request.POST.get('password'))
                login(request, new_user)
                return redirect('user_profile')
            except IntegrityError:
                return render(request, 'registration/registration.html', context={'unique_username':True})
        else:
            return render(request, 'registration/registration.html', context={'confirm_password':True})
    return render(request, 'registration/registration.html')
