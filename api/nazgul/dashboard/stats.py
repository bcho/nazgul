"""
    nazgul.dashboard.stats
    ~~~~~~~~~~~~~~~~~~~~~~

    Report stats.
"""

from flask import jsonify
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


@bp.route('/site/<string:netloc>', methods=['GET'])
def site(netloc):
    return render_template(
        'site.html',
        site=Site.query.filter_by(netloc=netloc).first_or_404())


@bp.route('/site/<string:netloc>/data', methods=['GET'])
def site_data(netloc):
    site = Site.query.filter_by(netloc=netloc).first_or_404()
    return jsonify({
        'visitor_actions': [a.to_dict() for a in site.visitor_actions]
    })
