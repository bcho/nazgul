"""
    nazgul.core.datetime
    ~~~~~~~~~~~~~~~~~~~~

    Datetime settings.
"""

import arrow


datetime = arrow.ArrowFactory(arrow.Arrow)
now = datetime.utcnow
