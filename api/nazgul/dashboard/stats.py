"""
    nazgul.dashboard.stats
    ~~~~~~~~~~~~~~~~~~~~~~

    Report stats.
"""

from flask import redirect
from flask import render_template
from flask import url_for

from ._base import bp

from nazgul.model import Site
from nazgul.model import VisitorLog


@bp.route('', methods=['GET'])
def redirect_to_stats():
    return redirect(url_for('.stats'), 301)


@bp.route('/stats', methods=['GET'])
def stats():
    return render_template(
        'stats.html',
        sites=Site.query.all(),
        visitors=VisitorLog.query.all())


@bp.route('/user/<string:uuid>', methods=['GET'])
def user(uuid):
    return render_template(
        'user.html',
        visitor=VisitorLog.query.filter_by(uuid=uuid).first_or_404())
