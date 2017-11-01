from rest_framework import serializers
from board.models import Post

class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('title', 'text', 'name', 'email', 'image')
