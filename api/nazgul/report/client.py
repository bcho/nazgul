"""
    nazgul.report.client
    ~~~~~~~~~~~~~~~~~~~~

    Client metric upload api.
"""

from flask import request

from nazgul.contrib.flask import cors
from nazgul.contrib.flask import returns_json

from ._base import bp


def extract_report(request):
    """Extract visitor report from request.

    Args:
        request: request instance.

    Returns:
        dict.
    """
    payload = request.get_json(force=True)
    return {
        'visitor_id': payload['visitor_id'],
        'action': payload['action'],
        'created_at': payload['created_at'],

        'url': payload['url'],
        'user_agent': request.user_agent,
        'referer': request.referrer,
        'ip': request.remote_addr,
    }


@bp.route('', methods=['POST', 'OPTIONS'])
@cors(headers=['content-type'])
@returns_json
def upload_report():
    extract_report(request)
    return {'code': 0}
