"""
    nazgul.model.entity
    ~~~~~~~~~~~~~~~~~~~

    Base entities.
"""

import enum

from nazgul.core.db import db

from ._base import BaseColumnsMixin
from ._base import EnumTypeMixin


class Site(BaseColumnsMixin, db.Model):
    """A site."""

    host = db.Column(db.String, unique=True)


class Url(BaseColumnsMixin, db.Model):
    """A url."""

    # Url should be `scheme://netloc/path`.
    url = db.Column(db.String, unique=True)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'))
    site = db.relationship('Site', backref=db.backref('urls'))


class VisitorActions(EnumTypeMixin, enum.Enum):

    # Visitor clicks on a link.
    CLICK = 'click'

    # Visitor submit a query.
    QUERY = 'query'


class VisitorAction(BaseColumnsMixin, db.Model):
    """An action."""

    name = db.Column(db.Enum(*VisitorActions._as_db_enum()), unique=True)
