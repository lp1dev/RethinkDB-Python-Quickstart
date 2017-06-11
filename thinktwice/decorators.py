from sanic.response import json


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
