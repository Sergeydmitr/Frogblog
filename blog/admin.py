from django.contrib import admin
from .models import Article, Fact, Comment

admin.site.register(Article)
admin.site.register(Fact)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'article', 'date', 'approved')
    list_filter = ('approved', 'date')
    search_fields = ('author', 'text')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
