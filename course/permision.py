from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True

        return False


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderator').exists()


class CanCreate(BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name='moderator').exists():
            return False

        return True


class IsCurrentUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj:

            return True

        return False