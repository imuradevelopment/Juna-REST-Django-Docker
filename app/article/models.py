import uuid as uuid_lib
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import length
from django.utils import timezone

User = get_user_model()

class Tag(models.Model):
    name = models.CharField('タグ名', max_length=50)
    def __str__(self):
        return self.name

class Article(models.Model):
    id = models.UUIDField(default=uuid_lib.uuid4,primary_key=True,editable=False)
    title = models.CharField('タイトル', max_length=120)
    author = models.ForeignKey(User, verbose_name="著者", on_delete=models.PROTECT)
    thumbnail = models.ImageField('サムネイル', blank=True, null=True)
    tag = models.ManyToManyField(Tag, verbose_name='タグ')
    main_text = models.TextField('本文')
    created_at= models.DateTimeField('作成日', auto_now_add=True)
    updated_on = models.DateTimeField('更新日', auto_now=True)
    #is_public = models.BooleanField('公開可能か', default=True)
    favorite = models.ManyToManyField(User, related_name='article_favorite', blank=True)

    class Meta:
        ordering = ('-created_at',)  # 新しいデータから表示される

    def __str__(self):
        return self.title

class Comment(models.Model):
    """記事に紐づくコメント"""
    text = models.TextField('コメント内容')
    target_article = models.ForeignKey(Article, verbose_name='対象記事', on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, verbose_name="コメンター", on_delete=models.PROTECT)
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.text[:20]

class Reply(models.Model):
    """コメントに紐づく返信"""
    text = models.TextField('リプライ内容')
    target_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='対象コメント')
    replyer = models.ForeignKey(User, verbose_name="コメンター", on_delete=models.PROTECT)
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.text[:20]
