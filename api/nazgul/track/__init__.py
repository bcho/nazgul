"""
    nazgul.track
    ~~~~~~~~~~~~

    Track scripts.
"""

# Load views.
from .resource import *  # noqa

from ._base import bp


def setup(app):
    app.register_blueprint(bp, url_prefix='/track/v1')

    return app
