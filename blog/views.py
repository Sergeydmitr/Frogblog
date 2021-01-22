from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
    PermissionRequiredMixin
)
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required, permission_required
from .models import Article, Comment
from .forms import CommentForm
import datetime

# def index(request):
#     data = {
#         'news' : Article.objects.all(),
#         'title' : 'Главная страница блога'
#     }
#     return render(request, 'blog/index.html', data)

class ShowAllArticles(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article'
    ordering = ['-date']
    paginate_by = 5

    def get_context_data(self, **kwards):
        ctx = super(ShowAllArticles, self).get_context_data(**kwards)
        ctx['title'] = 'Блог о жабах'
        return ctx

class ArticlesDetailView(FormMixin, DetailView):
    model = Article
    form_class = CommentForm


    def get_context_data(self, **kwards):
        ctx = super(ArticlesDetailView, self).get_context_data(**kwards)
        ctx['title'] = Article.objects.filter(pk=self.kwargs['pk']).first()
        ctx['comments'] = self.object.comment_set.filter(approved=True)
        ctx['form'] = CommentForm(initial={'post': self.object})

        return ctx


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            messages.success(request, f'Ваш комментарий будет добавлен после модерации')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def form_valid(self, form):
        form.instance.article = self.object
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('article-detail', kwargs={'pk': self.object.pk})


class CreateArticleView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'blog.add_article'
    model = Article
    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class EditArticleView(LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'blog.change_article'
    model = Article
    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# ПРОВЕРКА ПОЛЬЗОВАТЕЛЯ ПО ТАБЛИЦЕ

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.author:
            return True
        return False

class DeleteArticleView(LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'blog.delete_article'
    model = Article
    success_url = '/'

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.author:
            return True
        return False

class UserAllArticlesView(ListView):
    model = Article
    template_name = 'blog/user_articles.html'
    context_object_name = 'article'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Article.objects.filter(author=user).order_by('-date')

    def get_context_data(self, **kwards):
        ctx = super(UserAllArticlesView, self).get_context_data(**kwards)
        ctx['title'] = f"Все статьи автора {self.kwargs.get('username')}"
        return ctx


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    success_url = '/'


    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(CommentDeleteView, self).get_object()
        if not obj.author == self.request.user:
            raise Http404
        return obj


    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'Страница о сайте'})


def TableTest(request):
    return render(request, 'blog/tables.html', {'title': 'Таблица'})
