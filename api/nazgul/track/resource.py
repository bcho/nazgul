"""
    nazgul.track.resource
    ~~~~~~~~~~~~~~~~~~~~~

    Track resources.
"""

from flask import send_from_directory

from ._base import bp


@bp.route('/track.js', methods=['HEAD', 'OPTIONS', 'GET'])
def track_js():
    return send_from_directory(
        bp.root_path,
        'static/js/track.js'
    )
