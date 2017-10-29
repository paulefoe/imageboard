from rest_framework import serializers
from board.models import Post, Board, Thread


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('title', 'text', 'name', 'email', 'image', 'op', 'thread', 'board')


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'ip', 'text', 'name', 'email', 'image', 'op', 'bump', 'published', 'thread', 'board')


class PostUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('title', 'text', 'name')



