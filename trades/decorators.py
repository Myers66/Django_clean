from django.http import JsonResponse
from functools import wraps

def api_login_required(view_func):
    """
    Декоратор для API-представлений.
    Если пользователь не авторизован – возвращает 401 JSON.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'detail': 'Authentication required'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper

def require_auth_for_methods(methods):
    """
    Декоратор, который требует авторизацию только для указанных HTTP-методов.
    Например: @require_auth_for_methods(['POST', 'PUT', 'DELETE'])
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.method in methods and not request.user.is_authenticated:
                return JsonResponse({'detail': 'Authentication required'}, status=401)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator