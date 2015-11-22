"""
    nazgul.report.client
    ~~~~~~~~~~~~~~~~~~~~

    Client metric upload api.
"""

import json

from flask import abort
from flask import request

from nazgul.contrib.flask import returns_json

from ._base import bp


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
            'action': payload['action'],
            'created_at': payload['created_at'],

            'url': payload['url'],
            'user_agent': payload.get('user_agent', request.user_agent),
            'referer': payload.get('referer', request.referrer),
            'ip': request.remote_addr,

            'value': payload.get('value', {})
        }
    except ValueError:
        abort(400)


@bp.route('', methods=['GET'])
@returns_json
def upload_report():
    print(extract_report(request))
    return {'code': 0}
