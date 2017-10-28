from rest_framework import serializers
from .models import Post, Board, Thread
from rest_framework import permissions
import datetime


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('title', 'ip', 'text', 'name', 'email', 'image', 'op', 'bump', 'published', 'thread', 'board')


class BlacklistPermission(permissions.BasePermission):
    """
    Global permission check for blacklisted IPs.
    """

    def has_object_permission(self, request, view, obj):
        ip_addr = request.META['REMOTE_ADDR']
        diff = obj.published - datetime.datetime.now()
        return ip_addr == obj.ip and diff < 120
