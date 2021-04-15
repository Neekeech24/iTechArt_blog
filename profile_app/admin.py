from django.contrib import admin
from django.db.models import Count
from django.contrib.auth.admin import UserAdmin

from blog_app.admin import ArticleInline
from profile_app.models import UserModel


@admin.register(UserModel)
class UserAdmin(UserAdmin):
    inlines = [ArticleInline,]
    search_fields = ['username', 'first_name', 'last_name']
    list_filter = ['date_joined', 'is_staff', 'is_active']
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'articles_count')

    def articles_count(self, obj):
        return obj.articles_count
    articles_count.short_description = 'Кол-во статей'
    articles_count.empty_value_display = '-'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(articles_count=Count('article__id', distinct=True))
        return queryset

    class Meta:
        model = UserModel