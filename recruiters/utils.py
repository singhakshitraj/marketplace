from functools import wraps
from .middleware import CheckRecruiterAccountMiddleware

def apply_middleware(middleware_class):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            middleware_instance = middleware_class(lambda req: view_func(req, *args, **kwargs))
            return middleware_instance(request)
        return _wrapped_view
    return decorator