from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsOwnerOrAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True
        if hasattr(obj, "author"):
            return obj.author == request.user
        if hasattr(obj, "commenter"):
            return obj.commenter == request.user
        if hasattr(obj, "replyer"):
            return obj.replyer == request.user
