"""
    nazgul.cli
    ~~~~~~~~~~

    CLI entry point.
"""

import click

from nazgul.core.app import build


app = build()


@click.group()
def main():
    pass


@main.command()
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=5566)
def serve_api(host, port):
    """Serve api."""
    app.run(host=host, port=port, debug=True)


@main.command()
def init_db():
    """Initialize database."""
    from nazgul.model import db

    with app.app_context():
        db.create_all()
        click.echo('Init db done: {}'.format(db.engine))


if __name__ == '__main__':
    main()
