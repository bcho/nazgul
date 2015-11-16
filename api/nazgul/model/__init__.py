"""
    nazgul.model
    ~~~~~~~~~~~~

    Model definition.
"""

from .entity import Site  # noqa
from .entity import Url  # noqa
from .entity import VisitorActions  # noqa
from .entity import VisitorAction  # noqa
from .log import RefererType  # noqa
from .log import VisitorLog  # noqa
from .log import VisitorActionLog  # noqa

from ._base import db  # noqa
