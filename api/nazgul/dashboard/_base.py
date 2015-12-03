"""
    nazgul.dashboard._base
    ~~~~~~~~~~~~~~~~~~~~~~
"""

from flask import Blueprint


bp = Blueprint('dashboard', __name__, template_folder='template')
