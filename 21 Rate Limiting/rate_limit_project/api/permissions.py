from rest_framework import permissions
from .models import UserProfile

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Object-level permission to only allow owners to edit"""
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only to the owner
        return obj.created_by == request.user

class GroupBasedPermission(permissions.BasePermission):
    """Permission based on user's group/tier"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Get user's tier
        try:
            profile = request.user.profile
            group = profile.group
            tier = group.rate_limit_tier if group else 'free'
        except UserProfile.DoesNotExist:
            tier = 'free'
        
        # Check permission based on tier
        if request.method == 'GET':
            # All tiers can read
            return True
        elif request.method in ['POST', 'PUT', 'PATCH']:
            # Only basic tier and above can write
            return tier in ['basic', 'premium', 'enterprise']
        elif request.method == 'DELETE':
            # Only premium and enterprise can delete
            return tier in ['premium', 'enterprise']
        
        return False

class PremiumProductPermission(permissions.BasePermission):
    """Special permission for premium products"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Check if user has premium tier or specific permission
        try:
            profile = request.user.profile
            group = profile.group
            if group and group.rate_limit_tier in ['premium', 'enterprise']:
                return True
        except UserProfile.DoesNotExist:
            pass
        
        # Check Django permission
        return request.user.has_perm('api.can_view_premium_products')