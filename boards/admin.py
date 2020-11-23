from django.contrib import admin

# Register your models here.
from .models import Board, Post, Comment


class TimeAdmin(admin.ModelAdmin):
    readonly_fields = ('create_at', 'updated_at',)

admin.site.register(Board)
admin.site.register(Post, TimeAdmin)
admin.site.register(Comment, TimeAdmin)
