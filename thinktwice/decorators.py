from sanic.response import json
from users.model import User
import jwt
import config


def requires_login(f):
    def wrappee(*args, **kwargs):
        headers = args[0].headers
        if 'authorization' not in headers.keys():
            return json({'error': 'Missing Authorization header', 'code': 401}, status=401)
        try:
            json_user = jwt.decode(headers['authorization'], config.secret, algorithms=['HS256'])
        except jwt.exceptions.DecodeError as e:
            return json({'error': 'Invalid Authorization token', 'code': 401}, status=401)
        kwargs['logged_user'] = User.get(json_user['username'])
        return f(*args, **kwargs)

    return wrappee


class MandatoryParams(object):
    def __init__(self, params):
        self.params = params

    def __call__(self, original_func):
        def wrappee(*args, **kwargs):
            params = args[0].json
            for parameter in self.params:
                if parameter not in params:
                    return json({'error': 'missing parameter %s' % parameter, 'code': '400'}, status=400)
            return original_func(*args, **kwargs)

        return wrappee
