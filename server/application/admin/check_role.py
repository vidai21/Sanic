from functools import wraps

from sanic.response import json

def check_role(request):
    if not request.ctx.user.get("role"):
        return False
        
    if request.ctx.user.get("role") == "1":
        return True
    else:
        return False


def protected_admin(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_admin = check_role(request)

            if is_admin:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return json({
                    "message": "you are not admin!"
                }, status=401)

        return decorated_function

    return decorator(wrapped)