"""
    nazgul.core.app
    ~~~~~~~~~~~~~~~

    Application.
"""

from flask import Flask

from nazgul.core import db


builtin_modules = [
    db,
]


def setup_modules(app, *modules):
    """Setup app with modules.

    Args:
        app: application instance.
        *modules: modules to be setup.

    Returns:
        application instance.
    """
    for module in modules:
        app = module.setup(app)
    return app


def build(configs=None, modules=None):
    """Build application.

    Args:
        configs: extra application configurations.
        modules: extra modules.

    Returns:
        application instance.
    """
    configs = configs or {}
    assert isinstance(configs, dict)
    modules = modules or []
    assert isinstance(modules, (list, tuple))

    app = Flask(__name__)

    app.config.from_envvar('NAZGUL_API_CONFIG', silent=True)
    app.config.update(configs)

    setup_modules(app, *builtin_modules)
    setup_modules(app, *modules)

    return app
