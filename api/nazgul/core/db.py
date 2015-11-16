"""
    nazgul.core.db
    ~~~~~~~~~~~~~~

    Database connection.
"""

from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def setup(app):
    """Initialize database connection.

    Args:
        app: application instance.

    Returns:
        application instance.
    """
    db.init_app(app)

    return app
