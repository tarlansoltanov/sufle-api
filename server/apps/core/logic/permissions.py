from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Custom permission class to allow only admin users to edit an object."""

    def has_permission(self, request, view):
        """Return True if permission is granted."""
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_staff
