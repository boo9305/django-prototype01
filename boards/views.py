from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, views, generics, status
from rest_framework.response import Response

from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import BoardSerializer
from .serializers import PostSerializer, PostDetailSerializer , PostCreateSerializer
from .serializers import CommentSerializer

from .models import Board, Post, Comment

from django.contrib.auth.models import User

import math

class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    queryset = Board.objects.all()
    template_name =''

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    max_post = 10
    
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            #permission_classes = [IsAuthenticated]
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        elif self.action == 'create':
            return PostCreateSerializer
        else :
            return PostSerializer

    def list(self, request) :
        if 'page' in request.GET:
            page = int(request.GET['page'])
        else :
            page = 1

        if 'board'  in request.GET:
            board = int(request.GET['board'])

        page_start = (page - 1) * self.max_post;
        page_end = page * self.max_post
        queryset = Post.objects.filter(board=board).order_by('-create_at')[page_start:page_end]

        serializer = self.get_serializer(queryset, many=True)

        data = {} 
        data['posts'] = serializer.data
        data['count'] = queryset.count() 
        data['total_page'] = math.ceil(queryset.count() / self.max_post)
        return Response(data)

    def retrieve(self, request, pk=None):
        user = request.user
        post = get_object_or_404(self.queryset, pk=pk)
        post.views_up()

        serializer_class = self.get_serializer_class()
        post_serializer = serializer_class(post)
        
        comments = Comment.objects.filter(post=pk);
        comments_serializer = CommentSerializer(comments, many=True)
        
        try : 
            liked_user = post.likes.get(pk=user.pk)
            is_liked = True
        except User.DoesNotExist:
            is_liked = False

        resp = { 'post' : post_serializer.data , 'comments' : comments_serializer.data, 'is_liked' : is_liked}
        return Response(resp)

    def create(self, request):
        user = request.user
        data = request.data

        serializer_class = self.get_serializer_class()        
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        post = serializer.save(author=user)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [AllowAny] # release IsAuthenticated
    
    def create(self, request):
        user = request.user
        data = request.data
        post = get_object_or_404(Post.objects.all(), pk=data['post'])

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(author=user, post = post)
        
        comments_serialzier = CommentSerializer(post.comment, many=True)
        
        headers = self.get_success_headers(serializer.data)
        return Response(comments_serialzier.data, status=status.HTTP_201_CREATED, headers=headers)


class LikeAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user;
        pk = request.GET['post']
        post = Post.objects.all().get(pk=pk)

        try : 
            liked_user = post.likes.get(pk=user.pk)
            post.likes.remove(liked_user)
            is_liked = False
        except User.DoesNotExist:
            liked_user = None;
            post.likes.add(user)
            post.save()
            is_liked = True
            print("up likes")

        likes_count = post.likes.count()
        return Response({ 'likes_count' : likes_count, 'is_liked' : is_liked })

            
        

