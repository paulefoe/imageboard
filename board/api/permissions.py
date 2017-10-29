from rest_framework import permissions
from django.utils import timezone


class BlacklistPermission(permissions.BasePermission):
    message = 'You only can update the post that you created and only within 2 minutes'

    def has_object_permission(self, request, view, obj):
        ip_addr = request.META['REMOTE_ADDR']
        diff = timezone.now() - obj.published
        return ip_addr == obj.ip and diff.seconds < 120
