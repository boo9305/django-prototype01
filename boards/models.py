from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Board(models.Model):
    board_name = models.CharField(max_length=100)

    create_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return '%s' % (self.board_name)

class Post(models.Model):
    board = models.ForeignKey(Board, on_delete=models.SET_NULL, null=True, related_name="post")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="post")
    title = models.CharField(max_length=100)
    content = models.TextField()
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name="liked_post")

    create_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return '%d' % (self.pk)

    def views_up(self):
        self.views = self.views + 1
        self.save()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, related_name="comment")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="comment")
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name="liked_comment")

    create_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class PostImage(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="")

