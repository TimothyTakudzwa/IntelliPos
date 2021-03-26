from rest_framework import permissions

class IsMerchantAdminUser(permissions.BasePermission):
    """
    View-level permission to allow only merchant admin users.
    """
    message = 'Only Merchant Admin allowed.'

    def has_permission(self, request, view):
        return request.user.is_merchant_admin


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of the object.
    """

    message = 'Only Owner is allowed.'

    def has_object_permission(self, request, view, obj):
            return obj.user == request.user

