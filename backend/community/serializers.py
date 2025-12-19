from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    liked_count = serializers.IntegerField(source='liked_users.count', read_only=True)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
                    'id', 'post', 'author', 'author_username', 'content', 
                    'created_at', 'updated_at', 'liked_count', 'is_liked'
                ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
        
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.liked_users.filter(id=request.user.id).exists()
        return False

class PostListSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    liked_count = serializers.IntegerField(source='liked_users.count', read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'author_username', 'created_at', 
                  'view_count', 'comment_count', 'liked_count']
        read_only_fields = ['id', 'author', 'created_at', 'view_count']
    
class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    liked_count = serializers.IntegerField(source='liked_users.count', read_only=True)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'author_username', 
                  'created_at', 'updated_at', 'view_count', 'comment_count', 'liked_count', 'is_liked']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'view_count']
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.liked_users.filter(id=request.user.id).exists()
        return False
    
class PostDetailSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    liked_count = serializers.IntegerField(source='liked_users.count', read_only=True)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'author_username', 
                  'created_at', 'updated_at', 'view_count', 'comments', 'liked_count', 'is_liked']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'view_count']
        
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.liked_users.filter(id=request.user.id).exists()
        return False