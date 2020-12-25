from rest_framework import routers
from django.urls import path

from .views import BoardViewSet, PostViewSet, CommentViewSet, PostImageViewSet
from .views import LikeAPIView, SearchAPIView


router = routers.DefaultRouter()
router.register('board', BoardViewSet, basename='board')
router.register('post', PostViewSet, basename='post')
router.register('comment', CommentViewSet, basename='comment')
router.register('image', PostImageViewSet, basename='image')
#router.register('post_count', PostCountView, basename='post_count')

urlpatterns = [
        path('like/', LikeAPIView.as_view()),
        path('search/', SearchAPIView.as_view())
]
urlpatterns += router.urls
