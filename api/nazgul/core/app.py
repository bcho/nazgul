"""
    nazgul.core.app
    ~~~~~~~~~~~~~~~

    Application.
"""

from flask import Flask

from nazgul.core import db


_modules = [
    db,
]


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

    for builtin_module in _modules:
        app = builtin_module.setup(app)
    for module in modules:
        app = module.setup(app)

    return app
