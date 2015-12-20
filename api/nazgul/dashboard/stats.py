"""
    nazgul.dashboard.stats
    ~~~~~~~~~~~~~~~~~~~~~~

    Report stats.
"""

from collections import defaultdict
from urllib.parse import urlparse

import arrow
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import url_for
import vincent

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
        s = from_url.netloc or visitor_action.action_value.get('from_url')
        sites_to_this_site[s].append(visitor_action.to_dict())

    for url in site.urls:
        from_this_url = VisitorActionLog.query \
            .filter_by(url_ref_id=url.id).all()
        for visitor_action in from_this_url:
            # FIXME
            if visitor_action.action.enum_name is not VisitorActions.CLICK:
                continue
            dest_url = urlparse(visitor_action.action_value.get('dest_url'))
            s = dest_url.netloc or visitor_action.action_value.get('dest_url')
            sites_from_this_site[s].append(visitor_action.to_dict())

    to_chart = vincent.Pie({'{}: {}'.format(k, len(v)): len(v)
                            for k, v in sites_to_this_site.items()})
    to_chart.legend('站点')
    to_chart = to_chart.grammar()
    from_chart = vincent.Pie({'{}: {}'.format(k, len(v)): len(v)
                              for k, v in sites_from_this_site.items()})
    from_chart.legend('站点')
    from_chart = from_chart.grammar()

    return {
        'to': sites_to_this_site,
        'to_chart': to_chart,
        'from': sites_from_this_site,
        'from_chart': from_chart,
    }


def calculate_site_traffic(site):
    dates = sorted(list({i.created_at for i in site.visitor_actions}))
    if not dates:
        return

    actions_by_date = {}
    for date in arrow.Arrow.span_range('day', dates[0], dates[-1]):
        actions_by_date[date[0].format('MM-DD')] = 0
    for action in site.visitor_actions:
        date = action.created_at.format('MM-DD')
        actions_by_date[date] += 1

    chart = vincent.Bar(actions_by_date)
    chart.legend = '流量'
    chart.axis_titles(x='日期', y='请求数')
    return chart.grammar()


@bp.route('/site/<string:netloc>/data', methods=['GET'])
def site_data(netloc):
    site = Site.query.filter_by(netloc=netloc).first_or_404()
    return jsonify({
        'traffic_chart': calculate_site_traffic(site),
        'refers': calculate_site_refers(site),
    })
