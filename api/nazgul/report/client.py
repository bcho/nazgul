"""
    nazgul.report.client
    ~~~~~~~~~~~~~~~~~~~~

    Client metric upload api.
"""

import json

from flask import abort
from flask import request
from werkzeug import UserAgent

from nazgul.core.datetime import datetime
from nazgul.contrib.flask import returns_json

from nazgul.model import VisitorAction
from nazgul.model import VisitorActions

from nazgul.report.service import store

from ._base import bp


def extract_user_agent(payload):
    try:
        return UserAgent(payload.get('user_agent'))
    except Exception:
        pass


def extract_action(payload):
    return VisitorAction.from_enum(
        VisitorActions(payload['action'].strip().lower()))


def extract_report(request):
    """Extract visitor report from request.

    Args:
        request: request instance.

    Returns:
        dict.
    """
    try:
        payload = json.loads(request.values['data'])
        return {
            'visitor_id': payload['visitor_id'],
            'action': extract_action(payload),
            'created_at': datetime.get(payload['created_at']),

            'url': payload['url'],
            'user_agent': extract_user_agent(payload) or request.user_agent,
            'referer': payload.get('referer', request.referrer),
            'ip': request.remote_addr,

            'value': payload.get('value', {})
        }
    except ValueError:
        abort(400)


@bp.route('', methods=['GET'])
@returns_json
def upload_report():
    report = extract_report(request)
    store.store_report(report)
    return {'code': 0}
