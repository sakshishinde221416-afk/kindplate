from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse

def role_required(*allowed_roles):
    """Decorator to check if user has required role"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            if request.user.role not in allowed_roles:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('home')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def subscription_required(tier='pro'):
    """Decorator to check subscription tier"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            user_tier = request.user.get_subscription_tier()
            tier_hierarchy = {'free': 0, 'pro': 1, 'enterprise': 2}
            
            if tier_hierarchy.get(user_tier, 0) < tier_hierarchy.get(tier, 0):
                messages.error(request, f'This feature requires {tier.title()} subscription.')
                return redirect('subscription_plans')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def feature_required(feature_name):
    """Decorator to check if user has specific feature"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            if not request.user.has_feature(feature_name):
                messages.error(request, f'This feature is not available in your plan.')
                return redirect('subscription_plans')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def api_key_required(view_func):
    """Decorator for API authentication"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return JsonResponse({'error': 'API key required'}, status=401)
        
        # TODO: Validate API key from database
        
        return view_func(request, *args, **kwargs)
    return wrapper
