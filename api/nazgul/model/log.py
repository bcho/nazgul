"""
    nazgul.model.log
    ~~~~~~~~~~~~~~~~

    Vistor activities log.
"""

import enum
import json

from nazgul.core.datetime import now
from nazgul.core.db import db

from ._base import ArrowType
from ._base import BaseColumnsMixin
from ._base import EnumTypeMixin
from .entity import VisitorActions


class RefererType(EnumTypeMixin, enum.Enum):

    DIRECT_ENTRY = 'direct'
    # With referer url.
    WEBSITE = 'website'


class VisitorLog(BaseColumnsMixin, db.Model):
    """A visitor log."""

    # Client generated uuid.
    uuid = db.Column(db.String, unique=True)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'))
    site = db.relationship('Site', backref=db.backref('visitor_logs'))

    # Visitor metric.
    visit_count = db.Column(db.Integer, default=0)
    first_visit_time = db.Column(ArrowType, default=now)
    last_visit_time = db.Column(ArrowType, default=now)
    first_action_time = db.Column(ArrowType, default=now)
    last_action_time = db.Column(ArrowType, default=now)
    referer_type = db.Column(db.Enum(*RefererType._as_db_enum()))
    referer_url = db.Column(db.String)
    os = db.Column(db.String)
    browser = db.Column(db.String)
    ip = db.Column(db.String)

    @property
    def latest_action(self):
        if self.actions:
            return self.actions[-1]


class VisitorActionLog(BaseColumnsMixin, db.Model):
    """Visitor action log."""

    visitor_id = db.Column(db.Integer, db.ForeignKey('visitor_log.id'))
    visitor = db.relationship('VisitorLog', backref=db.backref('actions'))

    site_id = db.Column(db.Integer, db.ForeignKey('site.id'))
    site = db.relationship('Site', backref=db.backref('visitor_actions'))

    url_id = db.Column(db.Integer, db.ForeignKey('url.id'))
    url = db.relationship(
        'Url', primaryjoin='Url.id==VisitorActionLog.url_id')
    url_ref_id = db.Column(db.Integer, db.ForeignKey('url.id'))
    url_ref = db.relationship(
        'Url', primaryjoin='Url.id==VisitorActionLog.url_ref_id')

    action_id = db.Column(db.Integer, db.ForeignKey('visitor_action.id'))
    action = db.relationship(
        'VisitorAction',
        primaryjoin='VisitorAction.id==VisitorActionLog.action_id')
    action_ref_id = db.Column(db.Integer, db.ForeignKey('visitor_action.id'))
    action_ref = db.relationship(
        'VisitorAction',
        primaryjoin='VisitorAction.id==VisitorActionLog.action_ref_id')

    action_value_raw = db.Column('action_value', db.Text)

    @property
    def action_value(self):
        try:
            return json.loads(self.action_value_raw)
        except:
            pass

    def set_action_value(self, value):
        self.action_value_raw = json.dumps(value)

    def describe(self):
        if self.action.enum_name == VisitorActions.CLICK:
            dest_url = self.action_value['dest_url']
            return '点击 <a href="{}">{}</a>...'.format(
                dest_url, dest_url[:40])
        if self.action.enum_name == VisitorActions.QUERY:
            form_id = self.action_value.get('form_id')
            keyword = self.action_value.get('form_value')
            return '在表单 {} 中查询关键字 {}'.format(form_id, keyword)

    def to_dict(self):
        return {
            'site': self.site.netloc,
            'url': self.url.url,
            'action': self.action.name,
            'action_ref': self.action_ref.name,
            'action_value': self.action_value,
            'visitor_uuid': self.visitor.uuid,
            'created_at': self.created_at.isoformat(),
        }
