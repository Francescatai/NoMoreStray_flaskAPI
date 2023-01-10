from functools import wraps
from flask import g
from utils import restful


def permission_required(permission):
    def outter(func):
        @wraps(func)
        def inner(*args, **kwargs):
            user = getattr(g, "user")
            if not user:
                return restful.unlogin_error()
            if user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                return restful.permission_error(message="若需要使用功能權限請提出申請！")

        return inner

    return outter
