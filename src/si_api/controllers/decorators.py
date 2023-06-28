from functools import wraps

from quart import jsonify
from quart_jwt_extended import (
    verify_jwt_in_request, get_jwt_claims
)


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        print("Claims: {0}".format(claims))
        if claims['role'] != 'admin':
            return jsonify(msg='ACCESS DENIED!'), 403
        else:
            return fn(*args, **kwargs)

    return wrapper
