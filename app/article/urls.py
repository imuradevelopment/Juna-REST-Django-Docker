from django.urls import path
from . import views

app_name = 'article'

urlpatterns = [
    path('articles/', views.ArticleListView.as_view()),
    path('articles/create/', views.ArticleCreateView.as_view()),
    path('articles/<uuid:pk>/', views.ArticleRUDView.as_view()),
    path('articles/comments/create/', views.CommentCreateView.as_view()),
    path('articles/comments/<int:pk>/', views.CommentDestroyView.as_view()),
    path('articles/comments/replys/create/', views.ReplyCreateView.as_view()),
    path('articles/comments/replys/<int:pk>/', views.ReplyDestroyView.as_view()),
    path('tags/', views.TagListView.as_view()),
    path('articles/favorites/', views.ArticleFavoriteView.as_view())
]