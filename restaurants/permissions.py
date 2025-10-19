from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsRestaurantEditor(BasePermission):
    """Allow safe methods to anyone, mutations only to editor group."""

    editor_group = 'editors'

    def has_permission(self, request, view):  # noqa: ARG002
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.groups.filter(name=self.editor_group).exists()
