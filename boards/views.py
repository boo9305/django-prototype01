from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, views, generics, status, pagination
from rest_framework.response import Response

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from .serializers import BoardSerializer
from .serializers import PostSerializer, PostDetailSerializer , PostCreateSerializer, PostImageSerializer
from .serializers import CommentSerializer
from .serializers import LikeSerializer

from .models import Board, Post, Comment, PostImage

from .pagination import PostPagination

from django.contrib.auth.models import User

import math

class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    queryset = Board.objects.all()
    template_name =''
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    pagination_class = PostPagination
    queryset = Post.objects.all()
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
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

    def get_queryset(self):
        if self.action == 'list' :
            page = self.request.query_params.get('page', 1)
            board = self.request.query_params.get('board', 1)
            queryset = Post.objects.filter(board=board).order_by('-create_at')
        else :
            queryset = self.queryset;
        return queryset

    def retrieve(self, request, *args, **kwargs):
        post = get_object_or_404(self.queryset, pk=kwargs["pk"])
        post.views_up()
        return super().retrieve(request, args, kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny] # release IsAuthenticated
    pagination_class = PostPagination
    queryset = Comment.objects.all()
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    def perform_create(self,serializer) :
        user = self.request.user
        serializer.save(author=user)

    #def create(self, request, * args, **kwargs):
    #    serializer = self.get_serializer(data=request.data)
    #    serializer.is_valid(raise_exception=True)
    #    self.perform_create(serializer)
class SearchAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = PostPagination
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_response(self):
        return Response({})

    def get_queryset(self):
        search = self.request.query_params.get("search", "")
        search_type = self.request.query_params.get("type", "title")
        board = self.request.query_params.get('board', 1)
        
        if search_type == 'title' :
            queryset = Post.objects.filter(title__icontains=search, board=board).order_by('-create_at')
        else : 
            queryset = Post.objects.filter(title__icontains=search, board=board).order_by('-create_at')

        return queryset

class LikeAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LikeSerializer

    def get(self, request):
        user = request.user;
        pk = request.query_params.get('post')
        try : 
            post = Post.objects.all().get(pk=pk)
        except Post.DoesNotExist:
            return Response(data={'msg' : 'bad request'}, status=status.HTTP_400_BAD_REQUEST)

        try : 
            liked_user = post.likes.get(pk=user.pk)
            post.likes.remove(liked_user)
            is_liked = False
        except User.DoesNotExist:
            liked_user = None;
            post.likes.add(user)
            post.save()
            is_liked = True
        likes_count = post.likes.count()

        data = {
            'likes_count' : likes_count,
            'is_liked' : is_liked
                }
        serializer = self.get_serializer(instance=data)

        return Response(serializer.data, status=status.HTTP_200_OK)

            
class PostImageViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = PostImageSerializer
    queryset = PostImage.objects.all()

