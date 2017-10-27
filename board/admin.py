from django.contrib import admin
from .models import Post, Thread, Board


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'published', 'op', 'thread_id', 'title', 'text')


class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'description')


class ThreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_closed', 'is_pinned', 'published')

admin.site.register(Post, PostAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Board, BoardAdmin)

