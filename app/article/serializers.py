from rest_framework import serializers
from .models import Article, Tag, Comment, Reply
from account.models import User

class TagSerializer(serializers.ModelSerializer):
    """
    タグのシリアライザー
    """
    class Meta:
        model = Tag
        fields = '__all__'

class TagListSerializer(serializers.ListSerializer):
    """
    タグのリストシリアライザー
    """
    child = TagSerializer()

class ReplySerializer(serializers.ModelSerializer):
    target_comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all())
    replyer = serializers.ReadOnlyField(source='replyer.user_id')

    class Meta:
        model = Reply
        #fields = ('text', 'target_comment', 'replyer', 'created_at')
        fields = '__all__'
        read_only_fields = ('created_at',)

class CommentSerializer(serializers.ModelSerializer):
    target_article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all())
    commenter = serializers.ReadOnlyField(source='commenter.user_id')
    reply_set = ReplySerializer(read_only=True, many=True)
    class Meta:
        model = Comment
        #fields = ('text', 'target_article', 'commenter', 'created_at', 'reply_set')
        fields = '__all__'
        read_only_fields = ('created_at',)

class ArticleSerializer(serializers.ModelSerializer):
    """
    記事の詳細データ取得ビューでシリアライザー
    """
    tag = TagListSerializer()
    author = serializers.ReadOnlyField(source='author.user_id')
    favorite = serializers.StringRelatedField(read_only=True, many=True)
    comment_set = CommentSerializer(read_only=True, many=True)
    favorite_count = serializers.SerializerMethodField('get_favorite_count')

    class Meta:
        model = Article
        fields = '__all__'

    def create(self, validated_data):
        tags = []
        # 関連先のオブジェクトの登録
        for tag_data in validated_data.pop('tag'):
            tag, _ = Tag.objects.get_or_create(**tag_data)
            tags.append(tag)
        # 関連先オブジェクトとの関連レコードを登録
        article = super().create(validated_data)
        article.tag.set(tags)
        return article

    def update(self, instance, validated_data):
        tags = []
        # 関連先のオブジェクトの登録
        for tag_data in validated_data.pop('tag'):
            tag, _ = Tag.objects.get_or_create(**tag_data)
            tags.append(tag)
        # 関連先オブジェクトとの関連レコードを登録
        article = super().update(instance, validated_data)
        article.tag.set(tags)
        return article

    def get_favorite_count(self, instance):
        return instance.favorite.count()

class ArticleDescriptionSerializer(serializers.ModelSerializer):
    """
    記事一覧ビューで使う記事モデルのシリアライザー
    """
    tag = TagListSerializer(read_only=True)
    author = serializers.ReadOnlyField(source='author.user_id')
    favorite = serializers.StringRelatedField(many=True)
    favorite_count = serializers.SerializerMethodField('get_favorite_count')

    class Meta:
        model = Article
        exclude = ('main_text',)

    def get_favorite_count(self, instance):
        return instance.favorite.count()