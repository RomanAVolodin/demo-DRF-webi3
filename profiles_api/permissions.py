from rest_framework.permissions import BasePermission, SAFE_METHODS


class UpdateOwnProfile(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.id == request.user.id


class UpdateOwnStatus(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.user_profile.id == request.user.id
