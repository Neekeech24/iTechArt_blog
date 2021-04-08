from django.contrib import admin
from django.db.models import Count

from .models import Article, Comment
# Register your models here.

class CommentInline(admin.TabularInline):
    raw_id_fields = ['auth_user']
    model = Comment
    extra = 1


class ArticleInline(admin.StackedInline):
    model = Article
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Статья', {'fields':['theme', 'text']}),
        ('Информация',    {'fields':['author','pub_date', 'get_comment_count', 'get_rating_count']})
    ]
    inlines = [CommentInline]
    readonly_fields = ['get_comment_count', 'get_rating_count', 'pub_date']
    list_display = ('theme', 'pub_date', 'author', 'get_comment_count', 'get_rating_count')
    list_filter = ['pub_date']
    search_fields = ['text', 'theme']
    raw_id_fields = ['author']


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(comment_count=Count('comment__id', distinct=True),
                                     rating_count=Count('rating__id', distinct=True))
        return queryset

    class Meta:
        model = Article


admin.site.register(Comment)