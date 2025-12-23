from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow authors of a post to edit or delete it.
    Read-only methods (GET, HEAD, OPTIONS) are allowed for everyone.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
        if request.method in SAFE_METHODS:
            return True  # Allow read-only methods for anyone

        # Otherwise, only allow if the current user is the author
        return obj.author == request.user
