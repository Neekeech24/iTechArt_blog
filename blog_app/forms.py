from django import forms
from .models import Article, Comment


class CreateArticleForm(forms.ModelForm):
    theme = forms.CharField(max_length=128, help_text='Укажите тему статьи',
                            label='theme', required=True)
    text = forms.CharField(help_text='Текст статьи', widget=forms.Textarea, required=True)

    class Meta:
        model = Article
        fields = ['theme', 'text', 'author']
