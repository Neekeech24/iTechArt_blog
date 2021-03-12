from django import forms
from django.contrib.auth.models import User

from .models import Article, Comment


class CreateArticleForm(forms.ModelForm):
    theme = forms.CharField(max_length=128, help_text='Укажите тему статьи',
                            label='theme', required=True)
    text = forms.CharField(help_text='Текст статьи', widget=forms.Textarea, required=True)

    class Meta:
        model = Article
        fields = ['theme', 'text', 'author']


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
