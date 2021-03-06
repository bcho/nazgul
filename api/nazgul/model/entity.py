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

    netloc = db.Column(db.String(512), unique=True)

    @property
    def total_clients(self):
        client_count = 0
        for url in self.urls:
            client_count += len(url.visitor_logs)
        return client_count


class Url(BaseColumnsMixin, db.Model):
    """A url."""

    # Url should be `scheme://netloc/path`.
    url = db.Column(db.String(512), unique=True)
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

    @property
    def enum_name(self):
        return VisitorActions(self.name)

    @classmethod
    def init_db(cls, db):
        for action in VisitorActions:
            action_record = cls()
            action_record.name = str(action.value)
            db.session.add(action_record)
        db.session.commit()

    @classmethod
    def from_enum(cls, e):
        rv = cls.query.filter_by(name=e.value).first()
        assert rv is not None
        return rv
