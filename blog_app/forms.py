from django import forms
from django.contrib.auth.models import User

from .models import Article, Comment


class CreateArticleForm(forms.ModelForm):
    theme = forms.CharField(max_length=128, help_text='Укажите тему статьи',
                            label='theme', required=True)
    text = forms.CharField(help_text='Текст статьи', widget=forms.Textarea, required=True)

    def clean(self):
        super().clean()
        try:
            if Article.objects.filter(theme=self.cleaned_data['theme']).exists():
                self.add_error('theme', 'Статья с указанной темой уже существует.')
            return self.cleaned_data
        except KeyError:
            return self.cleaned_data


    class Meta:
        model = Article
        fields = ['theme', 'text', 'author']


class CreateCommentForm(forms.ModelForm):
    article = forms.ModelChoiceField(queryset=Article.objects.all())
    body = forms.CharField(widget=forms.Textarea, required=True, help_text='Ваш комментарий')
    auth_user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    anon_user = forms.CharField(required=False)

    class Meta:
        model = Comment
        fields = ['auth_user', 'anon_user', 'article', 'body', 'username']
