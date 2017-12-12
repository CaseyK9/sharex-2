from rest_framework.permissions import BasePermission

class IsCustomerAccount(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            return False
        return (not request.user.is_driver) or request.user.is_admin


class IsDriverAccount(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            return False
        return request.user.is_driver or request.user.is_admin


class IsAuthenticated(BasePermission):
	
	def has_permission(self, request, view):
		return request.user.is_authenticated()
		