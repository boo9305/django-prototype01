from rest_framework import serializers, exceptions

from .models import Board, Post, Comment, PostImage

from django.contrib.auth.models import User

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board;
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    create_at = serializers.DateTimeField(read_only=True, format="%H.%m.%d %H:%M:%S")

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'create_at']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)

    create_at = serializers.DateTimeField(read_only=True, format="%H-%m-%d %H:%M:%S")

    class Meta:
        model = Post;
        fields = ['id', 'author', 'title', 'board', 'views', 'is_liked', 'likes_count', 'comments_count', 'create_at']

    def get_comments_count(self, post):
        return post.comment.count()
    
    def get_is_liked(self, post):
        request = self.context.get("request")
        is_liked = False
        if request and hasattr(request, 'user'):
            print(is_liked)
            try :
                print(is_liked)
                liked_user = post.likes.get(pk=request.user.pk)
                is_liked = True
            except User.DoesNotExist:
                is_liked = False

        print(is_liked)
        return is_liked;
    
    def get_likes_count(self, post):
        return post.likes.count()

class PostDetailSerializer(PostSerializer):
    comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post;
        fields = ['id', 'author', 'title', 'board', 'content', 'views', 'is_liked' , 'likes_count', 'comment', 'create_at']


class PostCreateSerializer(PostSerializer):
    class Meta:
        model = Post;
        fields = ['title', 'content', 'board']

class LikeSerializer(serializers.Serializer):
    likes_count = serializers.IntegerField(default=0);
    is_liked = serializers.BooleanField(default=False);

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['name' , 'image']

