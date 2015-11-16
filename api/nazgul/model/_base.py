"""
    nazgul.model._base
    ~~~~~~~~~~~~~~~~~~
"""

from collections import Iterable
from datetime import datetime

from sqlalchemy import types

from nazgul.core.datetime import now
from nazgul.core.datetime import datetime as arrow_datetime
from nazgul.core.db import db


class ScalarCoercible(object):

    def _coerce(self, value):
        raise NotImplementedError

    def coercion_listener(self, target, value, oldvalue, initiator):
        return self._coerce(value)


class ArrowType(types.TypeDecorator, ScalarCoercible):

    impl = types.DateTime

    def process_bind_param(self, value, dialect):
        if value:
            return self._coerce(value).to('UTC').naive
        return value

    def process_result_value(self, value, dialect):
        if value:
            return arrow_datetime.get(value)
        return value

    def _coerce(self, value):
        if value is None:
            return None
        elif isinstance(value, str):
            value = arrow_datetime.get(value)
        elif isinstance(value, Iterable):
            value = arrow_datetime.get(*value)
        elif isinstance(value, datetime):
            value = arrow_datetime.get(value)
        return value


class BaseColumnsMixin(object):
    """Shared columns."""

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(ArrowType, default=now)
    updated_at = db.Column(ArrowType, onupdate=now)
    deleted_at = db.Column(ArrowType)


class EnumTypeMixin(object):

    @classmethod
    def _as_db_enum(cls):
        return [str(i.value) for i in cls]
