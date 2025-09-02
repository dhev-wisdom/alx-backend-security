from functools import wraps
from django_ratelimit.decorators import ratelimit

def user_based_rate_limit(view_func):
    """
    Apply 10/m for authenticated users, 5/m for anonymous users
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            decorator = ratelimit(key="ip", rate="10/m", method="POST", block=True)
        else:
            decorator = ratelimit(key="ip", rate="5/m", method="POST", block=True)
        return decorator(view_func)(request, *args, **kwargs)
    return _wrapped_view
