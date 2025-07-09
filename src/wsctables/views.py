# pylint: disable=duplicate-code
"""Basic app endpoints for wscearth"""

import logging

import flask
import flask_cachecontrol
import simplejson as json

# Circular import recommended here: https://flask.palletsprojects.com/en/3.0.x/patterns/packages/
from wsctables import app, cache  # pylint: disable=cyclic-import

logger = logging.getLogger(__name__)


@app.route("/")
@cache.cached(timeout=30)
@flask_cachecontrol.cache_for(seconds=30)
def index():
    """Render a Google map"""
    return flask.render_template("positions_map.html")


@app.route("/scripts/positions.js")
@cache.cached()
def positions_script():
    """Templated positions.js to allow for base URL rendering"""
    return flask.render_template("positions.js.j2")


@app.route("/api/path/")
@cache.cached(timeout=30)
@flask_cachecontrol.cache_for(seconds=30)
def api_path():
    """Render JSON path positions for car"""

    return json.dumps(
        {
            "sample": "data",
        },
    )


@app.route("/api/positions")
@cache.cached(timeout=30)
@flask_cachecontrol.cache_for(seconds=30)
def api_positions():
    """Render a positions JSON"""

    return json.dumps(
        {
            "sample": 1,
            "data": 2,
        },
        ignore_nan=True,
    )
