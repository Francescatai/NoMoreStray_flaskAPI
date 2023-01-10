# Restful API
from flask import jsonify


class HttpCode(object):
    # 狀態正常
    ok = 200
    # 沒有登入
    unloginerror = 401
    # 沒有權限
    permissionerror = 403
    # 客戶端參數錯誤
    paramserror = 400
    # 伺服器錯誤
    servererror = 500


def _restful_result(code, message, data):
    return jsonify({"message": message or "", "data": data or {}, "code": code})


def ok(message=None, data=None):
    return _restful_result(code=HttpCode.ok, message=message, data=data)


def unlogin_error(message="沒有登入！"):
    return _restful_result(code=HttpCode.unloginerror, message=message, data=None)


def permission_error(message="没有權限！"):
    return _restful_result(code=HttpCode.paramserror, message=message, data=None)


def params_error(message="參數錯誤！"):
    return _restful_result(code=HttpCode.paramserror, message=message, data=None)


def server_error(message="伺服器錯誤！"):
    return _restful_result(code=HttpCode.servererror, message=message or '伺服器內部錯誤', data=None)
