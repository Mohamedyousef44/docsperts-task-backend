from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsAuthor(permissions.BasePermission):
    """
    Custom permission class for checking if the user is the author of an object.

    This permission class allows safe HTTP methods (GET, HEAD, OPTIONS) to all users,
    but requires that the user is the author of the object for any other HTTP method.
    If the user is not the author of the object, a PermissionDenied exception is raised.

    Args:
        permissions (rest_framework.permissions.BasePermission): The base permission class to extend.

    Returns:
        bool: True if the user has permission to access the object, False otherwise.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the requesting user is the author of the object.

        Args:
            request (django.http.HttpRequest): The incoming HTTP request.
            view (django.views.View): The view handling the request.
            obj (django.db.models.Model): The object being accessed.

        Returns:
            bool: True if the user has permission to access the object, False otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            # Allow safe methods (GET, HEAD, OPTIONS) to all users
            return True
        else:
            # Check if the requesting user is the author of the object
            if obj.author != request.user:
                # Raise a PermissionDenied exception if the user is not the author
                raise PermissionDenied(
                    "You do not have permission to access this resource."
                )
            return True
