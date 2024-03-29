"""app.py

This is the entry file for the application, and
should only contain setup and boilerplate code.
"""
import dash_bootstrap_components as dbc
from dash_extensions.enrich import Dash
from flask_caching import Cache

app = Dash(
    __name__,
    title='Dashboard',
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{
        'name': 'viewport',
        'content': 'width=device-width, initial-scale=1.0'
    }],
)

cache = Cache(
    app.server,
    config={
        'CACHE_TYPE': 'FileSystemCache',
        'CACHE_DIR': 'file_system_store',
        'CACHE_DEFAULT_TIMEOUT': 180,
    },
)
