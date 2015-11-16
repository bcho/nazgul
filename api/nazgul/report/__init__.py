"""
    nazgul.report
    ~~~~~~~~~~~~~

    Report module.
"""

# Load views.
from .client import *  # noqa

from ._base import bp


def setup(app):
    app.register_blueprint(bp, url_prefix='/api/v1/report')

    return app
