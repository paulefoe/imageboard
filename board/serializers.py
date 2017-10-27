from rest_framework import serializers
from .models import Post, Board, Thread


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('title', 'ip', 'text', 'name', 'email', 'image', 'op', 'bump', 'published', 'thread', 'board')
