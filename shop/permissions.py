from rest_framework.permissions import BasePermission

class IsSellerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('GET'):
            return True
        return obj.seller == request.user