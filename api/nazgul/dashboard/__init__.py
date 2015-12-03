"""
    nazgul.dashboard
    ~~~~~~~~~~~~~~~~

    Dashboard module.
"""

# Load views.
from .stats import *  # noqa

from ._base import bp


def setup(app):
    app.register_blueprint(bp, url_prefix='/dashboard')

    return app
