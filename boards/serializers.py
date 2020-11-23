from rest_framework import serializers, exceptions

from .models import Board, Post, Comment

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board;
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    board = serializers.StringRelatedField(read_only=True)

    comments_count = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)

    create_at = serializers.DateTimeField(read_only=True, format="%H-%m-%d %H:%M:%S")

    class Meta:
        model = Post;
        fields = ['id', 'author', 'title', 'board', 'views', 'likes_count', 'comments_count', 'create_at']

    def get_comments_count(self, post):
        return post.comment.count()
    
    def get_likes_count(self, post):
        return post.likes.count()

class PostDetailSerializer(PostSerializer):

#    is_liked  = serializers.SerializerMethodField(read_only=True)
#    def get_is_liked(self, post):
#        liked_user = post.likes.filter(pk=user.pk).count()
#        if liked_user == 0:
#            return False
#        else :
#            return True;

    class Meta:
        model = Post;
        fields = ['id', 'author', 'title', 'board', 'content', 'views',  'likes_count', 'comments_count', 'create_at']

class PostCreateSerializer(PostSerializer):
    class Meta:
        model = Post;
        fields = ['title', 'content', 'board']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    post = serializers.StringRelatedField(read_only=True)

    create_at = serializers.DateTimeField(read_only=True, format="%H.%m.%d %H:%M:%S")

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'create_at']
