"""
    nazgul.cli
    ~~~~~~~~~~

    CLI entry point.
"""

import click

from nazgul.core.app import build
from nazgul.core.app import setup_modules


app = build()


@click.group()
def main():
    pass


@main.command()
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=5566)
def serve_api(host, port):
    """Serve api."""
    from nazgul import dashboard
    from nazgul import report

    api_app = setup_modules(
        app,
        report,
        dashboard
    )

    api_app.run(host=host, port=port, debug=True)


@main.command()
def init_db():
    """Initialize database."""
    from nazgul.model import db
    from nazgul.model import VisitorAction

    with app.app_context():
        db.drop_all()
        db.create_all()
        click.echo('Init db done: {}'.format(db.engine))

        VisitorAction.init_db(db)


if __name__ == '__main__':
    main()
