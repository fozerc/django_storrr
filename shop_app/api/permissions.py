from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in ['GET', 'HEAD'] or request.user.is_superuser


class IsAdminReturnActions(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'approve' or view.action == 'decline':
            return request.user.is_superuser
        return request.user.is_authenticated
