"""
    nazgul.contrib.flask
    ~~~~~~~~~~~~~~~~~~~~

    Flask utilities.
"""

from functools import wraps

from flask import jsonify


def returns_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        rv = func(*args, **kwargs)
        if isinstance(rv, dict):
            return jsonify(**rv)
        return rv
    return wrapper
