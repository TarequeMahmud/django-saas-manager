from accounts.models import Membership, Organization
from rest_framework.permissions import BasePermission


def get_user_role(user, organization: Organization) -> str | None:
    try:
        return Membership.objects.get(user=user, organization=organization).role

    except Membership.DoesNotExist:
        return None


class IsOrgMember(BasePermission):
    """
    Allow if the user is at least a MEMBER of the target organization.
    Assumes the view sets `self.organization` in `get_object()` or `get_organization()`.
    """

    def has_permission(self, request, view) -> bool:  # type: ignore[override]
        org = getattr(view, "organization", None)
        if org is None:
            return True
        role = get_user_role(request.user, org)
        return role is not None


class IsOrgManagerOrAdmin(BasePermission):
    """
    Allow Manager or Admin
    """

    def has_permission(self, request, view):  # type: ignore[override]
        org = getattr(view, "organization", None)
        if org is None:
            return False
        role = get_user_role(request.user, org)
        return role in {"MANAGER", "ADMIN"}


class IsOrgAdmin(BasePermission):
    """
    Allow only Admin
    """

    def has_permission(self, request, view):  # type: ignore[override]
        org = getattr(view, "organization", None)
        if org is None:
            return False
        role = get_user_role(request.user, org)
        return role == "ADMIN"
