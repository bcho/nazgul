"""
    nazgul.report.service.store
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Metric storage service.
"""

from urllib.parse import urlparse

from nazgul.contrib.multimethod import multimethod

from nazgul.model import db
from nazgul.model import RefererType
from nazgul.model import Site
from nazgul.model import Url
from nazgul.model import VisitorActionLog
from nazgul.model import VisitorActions
from nazgul.model import VisitorLog


def store_site(netloc):
    site = Site.query.filter_by(netloc=netloc).first()
    if not site:
        site = Site()
        site.netloc = netloc
        db.session.add(site)
        db.session.commit()
    return site


def store_url(url):
    """Store a url.

    Args:
        url: source url, will be cleaned into `scheme://netlocpath`

    Returns:
        ~`nazgul.model.Url`
    """
    parsed_url = urlparse(url)
    cleaned_url = '{scheme}://{netloc}{path}'.format(
        scheme=parsed_url.scheme,
        netloc=parsed_url.netloc,
        path=parsed_url.path)

    url = Url.query.filter_by(url=cleaned_url).first()
    if not url:
        site = store_site(parsed_url.netloc)
        url = Url()
        url.url = cleaned_url
        url.site = site
        db.session.add(url)
        db.session.commit()
    return url


def store_visitor(report):
    """Store a visitor.

    Args:
        report: visitor report activity.

    Returns:
        ~`nazgul.model.Visitor`
    """
    visitor = VisitorLog.query.filter_by(uuid=report['visitor_id']).first()
    if not visitor:
        visitor = VisitorLog()

        visitor.uuid = report['visitor_id']
        visitor.visit_count = 0

        visitor.site = report['url'].site

        visitor.first_visit_time = report['created_at']
        visitor.first_action_time = report['created_at']

        visitor.referer_url = report["referer"]
        if visitor.referer_url == "":
            visitor.referer_type = RefererType.DIRECT_ENTRY.value
        else:
            visitor.referer_type = RefererType.WEBSITE.value

        ua = report['user_agent']
        visitor.os = ua.platform
        visitor.browser = '{} {}'.format(ua.browser, ua.version)

        visitor.ip = report['ip']
        db.session.add(visitor)
        db.session.commit()

    visitor.visit_count = visitor.visit_count + 1
    visitor.last_visit_time = report['created_at']
    visitor.last_action_time = report['created_at']
    db.session.commit()

    return visitor


@multimethod
def store_action(report):
    return VisitorActions(report['action'].name)


def _store_action_basic(report):
    log = VisitorActionLog()
    log.visitor = report['visitor']
    log.site = report['url'].site
    log.url = report['url']
    log.action = report['action']
    log.set_action_value(report.get('value'))

    last_action = log.visitor.latest_action
    if last_action:
        log.url_ref = last_action.url
        log.action_ref = last_action.action

    db.session.add(log)
    db.session.commit()

    return log


@store_action.on(VisitorActions.CLICK)
def store_click_action(report):
    return _store_action_basic(report)


@store_action.on(VisitorActions.QUERY)
def store_query_action(report):
    return _store_action_basic(report)


def store_report(report):
    """Store a report."""
    # Clone report as context.
    report = report.copy()

    report['url'] = store_url(report['url'])
    report['visitor'] = store_visitor(report)
    report['action'] = store_action(report)

    return report
