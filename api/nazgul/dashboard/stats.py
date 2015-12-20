"""
    nazgul.dashboard.stats
    ~~~~~~~~~~~~~~~~~~~~~~

    Report stats.
"""

from collections import defaultdict
from urllib.parse import urlparse

from flask import jsonify
from flask import redirect
from flask import render_template
from flask import url_for

from ._base import bp

from nazgul.model import Site
from nazgul.model import VisitorLog
from nazgul.model import VisitorActionLog
from nazgul.model import VisitorActions


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


def calculate_site_refers(site):
    sites_to_this_site = defaultdict(list)
    sites_from_this_site = defaultdict(list)

    to_this_site = VisitorActionLog.query.filter_by(site_id=site.id).all()
    for visitor_action in to_this_site:
        # FIXME
        if visitor_action.action.enum_name is not VisitorActions.CLICK:
            continue
        from_url = urlparse(visitor_action.action_value.get('from_url'))
        s = from_url.netloc
        sites_to_this_site[s].append(visitor_action.to_dict())

    for url in site.urls:
        from_this_url = VisitorActionLog.query \
            .filter_by(url_ref_id=url.id).all()
        for visitor_action in from_this_url:
            # FIXME
            if visitor_action.action.enum_name is not VisitorActions.CLICK:
                continue
            dest_url = urlparse(visitor_action.action_value.get('dest_url'))
            s = dest_url.netloc
            sites_from_this_site[s].append(visitor_action.to_dict())

    return {
        'to': sites_to_this_site,
        'from': sites_from_this_site,
    }


@bp.route('/site/<string:netloc>/data', methods=['GET'])
def site_data(netloc):
    site = Site.query.filter_by(netloc=netloc).first_or_404()
    return jsonify({
        'visitor_actions': [a.to_dict() for a in site.visitor_actions],
        'refers': calculate_site_refers(site),
    })
