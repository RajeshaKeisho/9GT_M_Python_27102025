from rest_framework.throttling import SimpleRateThrottle
from django.core.cache import cache
from .models import UserProfile

class AnonRateThrottleCustom(SimpleRateThrottle):
    """Custom anonymous user rate limiting"""
    scope = 'anon_custom'
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return None  # No throttling for authenticated users
        
        # Get IP address
        ip = self.get_ident(request)
        
        # Different limits for different endpoints
        view_name = view.__class__.__name__
        if 'ProductListView' in view_name:
            self.rate = '30/minute'  # More lenient for product listing
        else:
            self.rate = '10/minute'  # Stricter for other endpoints
        
        return self.cache_format % {
            'scope': self.scope,
            'ident': f"ip:{ip}:{view_name}"
        }

class UserRateThrottleCustom(SimpleRateThrottle):
    """Custom user rate limiting"""
    scope = 'user_custom'
    
    def get_cache_key(self, request, view):
        if not request.user.is_authenticated:
            return None
        
        user_id = request.user.pk
        view_name = view.__class__.__name__
        
        return self.cache_format % {
            'scope': self.scope,
            'ident': f"user:{user_id}:{view_name}"
        }

class GroupBasedThrottle(SimpleRateThrottle):
    """Rate limiting based on user's group/tier"""
    scope = 'group_based'
    
    def get_cache_key(self, request, view):
        if not request.user.is_authenticated:
            return None
        
        # Get user's profile and group
        try:
            profile = request.user.profile
            group = profile.group
            tier = group.rate_limit_tier if group else 'free'
        except UserProfile.DoesNotExist:
            tier = 'free'
        
        # Set different rates based on tier
        tier_rates = {
            'free': '50/hour',
            'basic': '200/hour',
            'premium': '1000/hour',
            'enterprise': None  # Unlimited
        }
        
        self.rate = tier_rates.get(tier, '50/hour')
        
        # Return None for unlimited (enterprise tier)
        if self.rate is None:
            return None
        
        return self.cache_format % {
            'scope': self.scope,
            'ident': f"tier:{tier}:{request.user.pk}"
        }

class ScopedEndpointThrottle(SimpleRateThrottle):
    """Different rate limits for different endpoints/scopes"""
    
    def get_cache_key(self, request, view):
        # Get scope from view
        scope = getattr(view, 'throttle_scope', 'default')
        
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        
        return f"throttle_{scope}_{ident}"
    
    def allow_request(self, request, view):
        # Define scope-based rates
        scope = getattr(view, 'throttle_scope', 'default')
        
        scope_rates = {
            'product_list': '100/minute',     # High limit for listing
            'product_detail': '30/minute',    # Medium limit for details
            'product_create': '10/minute',    # Low limit for creation
            'order_create': '5/minute',       # Very low limit for orders
            'sensitive': '3/minute',          # Sensitive operations
            'default': '20/minute',           # Default rate
        }
        
        self.rate = scope_rates.get(scope, scope_rates['default'])
        return super().allow_request(request, view)

class CombinedThrottle:
    """Apply multiple throttles"""
    def __init__(self, throttle_classes):
        self.throttle_classes = throttle_classes
    
    def allow_request(self, request, view):
        # All throttles must pass
        for throttle_class in self.throttle_classes:
            throttle = throttle_class()
            if not throttle.allow_request(request, view):
                return False
        return True
    
    def wait(self):
        # Return the longest wait time
        wait_times = []
        for throttle_class in self.throttle_classes:
            throttle = throttle_class()
            if hasattr(throttle, 'wait'):
                wait_time = throttle.wait()
                if wait_time:
                    wait_times.append(wait_time)
        
        return max(wait_times) if wait_times else None