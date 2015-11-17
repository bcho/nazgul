"""
    nazgul.contrib.flask
    ~~~~~~~~~~~~~~~~~~~~

    Flask utilities.
"""

from datetime import timedelta
from functools import wraps
from functools import update_wrapper

from flask import current_app
from flask import jsonify
from flask import make_response
from flask import request


def returns_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        rv = func(*args, **kwargs)
        if isinstance(rv, dict):
            return jsonify(**rv)
        return rv
    return wrapper


class cors(object):
    """Enable CORS for a view.

    Args:
        origin: `Access-Control-Allow-Origin`, defaults to '*'.
        methods: `Access-Control-Allow-Methods`
        headers: `Access-Control-Allow-Headers`
        expose_headers: `Access-Control-Expose-Headers`
        maxage: `Access-Control-Max-Age`, defaults to 21600 (6 hrs).
    """

    def __init__(self, origin=None, methods=None, headers=None,
                 expose_headers=None, max_age=21600):
        self.origin = origin
        self.methods = methods
        self.headers = headers
        self.expose_headers = expose_headers
        self.max_age = max_age

        if self.origin is None:
            self.origin = '*'
        if isinstance(self.origin, (list, tuple)):
            self.origin = ', '.join(origin)

        if isinstance(self.methods, (tuple, list)):
            self.methods = ', '.join(sorted(x for x in self.methods))

        if isinstance(self.headers, (list, tuple)):
            self.headers = ', '.join(x for x in self.headers)

        if isinstance(self.expose_headers, (list, tuple)):
            self.expose_headers = ', '.join(x for x in self.expose_headers)

        if isinstance(max_age, timedelta):
            self.max_age = max_age.total_seconds()

    def get_allowed_methods(self):
        if self.methods is not None:
            return self.methods

        # Use default options response's setting.
        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def attach_headers(self, resp):
        h = resp.headers
        h['Access-Control-Allow-Origin'] = self.origin
        h['Access-Control-Allow-Methods'] = self.get_allowed_methods()
        h['Access-Control-Max-Age'] = str(self.max_age)
        if self.headers is not None:
            h['Access-Control-Allow-Headers'] = self.headers
        if self.expose_headers is not None:
            h['Access-Control-Expose-Headers'] = self.expose_headers

        return resp

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            # Pre-flight request.
            if request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            # Normal request.
            else:
                resp = make_response(func(*args, **kwargs))

            return self.attach_headers(resp)

        # Disable builtin options response.
        func.provide_automatic_options = False
        return update_wrapper(wrapper, func)
