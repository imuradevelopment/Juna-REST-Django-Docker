from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, pagination, response, status
from rest_framework.decorators import permission_classes
from rest_framework.utils.urls import remove_query_param, replace_query_param
from rest_framework.views import APIView

from .models import Article, Comment, Reply, Tag
from .serializers import (ArticleDescriptionSerializer, ArticleSerializer,
                          CommentSerializer, ReplySerializer,
                          TagSerializer)
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from .permissions import IsOwnerOrAdminOrReadOnly


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class ArticleCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ArticleRUDView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10

    # オーバーライドすると返されるJSONの内容に手を加える事ができる
    def get_paginated_response(self, data):
        return response.Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'totalPages': self.page.paginator.num_pages,
            'currentPage': self.page.number,
            'results': data,
            'pageSize': self.page_size,
            'rangeFirst': (self.page.number * self.page_size) - (self.page_size) + 1,
            'rangeLast': min((self.page.number * self.page_size), self.page.paginator.count),
        })

class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDescriptionSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.query_params.get('keyword', None)
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(lead_text__icontains=keyword) | Q(main_text__icontains=keyword))
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # subject = 'ブログにコメントがきました'
        # message = '記事にコメントがきました。管理画面から詳細を確認してください。'
        # from_email = settings.DEFAULT_FROM_EMAIL
        # recipient_list = [settings.DEFAULT_FROM_EMAIL]
        # send_mail(subject, message, from_email, recipient_list)
        return response

    def perform_create(self, serializer):
        serializer.save(commenter=self.request.user)

class CommentDestroyView(generics.DestroyAPIView):
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class ReplyCreateView(generics.CreateAPIView):
    serializer_class = ReplySerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # subject = 'ブログに返信がきました'
        # message = '記事に返信がきました。管理画面から詳細を確認してください。'
        # from_email = settings.DEFAULT_FROM_EMAIL
        # recipient_list = [settings.DEFAULT_FROM_EMAIL]
        # send_mail(subject, message, from_email, recipient_list)
        return response

    def perform_create(self, serializer):
        serializer.save(replyer=self.request.user)

class ReplyDestroyView(generics.DestroyAPIView):
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

class ArticleFavoriteView(APIView):
    permission_classes = [IsAuthenticated]
    bad_request_message = 'An error has occurred'

    def post(self, request):
        article = get_object_or_404(Article, pk=request.data.get('target_article'))
        if request.user not in article.favorite.all():
            article.favorite.add(request.user)
            return response.Response({'detail': 'User added to article'}, status=status.HTTP_200_OK)
        #return response.Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)
        return self.delete(request)

    def delete(self, request):
        article = get_object_or_404(Article, pk=request.data.get('target_article'))
        if request.user in article.favorite.all():
            article.favorite.remove(request.user)
            return response.Response({'detail': 'User removed from article'}, status=status.HTTP_204_NO_CONTENT)
        return response.Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)
