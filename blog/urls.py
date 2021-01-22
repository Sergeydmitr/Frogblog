from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShowAllArticles.as_view(), name='index'),
    path('user/<str:username>/', views.UserAllArticlesView.as_view(), name='user-articles'),
    path('article/<int:pk>/', views.ArticlesDetailView.as_view(), name='article-detail'),
    path('article/add/', views.CreateArticleView.as_view(), name='article-add'),
    path('article/<int:pk>/edit', views.EditArticleView.as_view(), name='article-edit'),
    path('article/<int:pk>/delete', views.DeleteArticleView.as_view(), name='article-delete'),
    path('about/', views.about, name='about'),
    path('delete-comment/<int:pk>', views.CommentDeleteView.as_view(), name='delete-comment'),
    path('table-test', views.TableTest, name='table-test')
]
