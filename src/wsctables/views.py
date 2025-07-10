# pylint: disable=duplicate-code
"""Basic app endpoints for wsctables."""

import logging

import flask
import flask_cachecontrol
import requests
import simplejson as json

# Circular import recommended here: https://flask.palletsprojects.com/en/3.0.x/patterns/packages/
from wsctables import app, cache  # pylint: disable=cyclic-import

logger = logging.getLogger(__name__)


@app.route("/")
#@cache.cached(timeout=30)
#@flask_cachecontrol.cache_for(seconds=30)
def index():
    """Render a table"""
    return flask.render_template("tables.html.j2")


@app.route("/scripts/wsctables.js")
#@cache.cached()
def tables_script():
    """Templated wsctables.js to allow for base URL rendering"""
    return flask.render_template("wsctables.js.j2")

@app.route("/api/scrutineering/")
#@cache.cached(timeout=30)
#@flask_cachecontrol.cache_for(seconds=30)
def scrutineering_script():
    """Templated positions.js to allow for base URL rendering"""
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQfPSSyRC2uuklVHGwzWLzrsEPmYYmF9dQVeHzGZQKIiovsyHAuSWATx3IDlMbqVBD1Scnbldv8rm9I/pub?gid=0&single=true&output=tsv' # pylint: disable=line-too-long
    r = requests.get(url, timeout=10)
    if r.status_code != 200:
        logger.error("Failed to fetch data from GitHub API: %s", r.status_code)
        return json.dumps({"error": "Failed to fetch data"}), 500

    # Parse the TSV data into a list of lines
    # Assuming the data is tab-separated values (TSV)

    result = {}

    header_txt = r.text.splitlines()[0]
    if not header_txt.strip():
        logger.error("No data found in the response header")
        return json.dumps({"error": "No data found"}), 500
    teamnames = header_txt.split("\t")

    for line in r.text.splitlines()[1:]:
        if not line.strip():
            continue

        # Split the line into columns
        columns = line.split("\t")

        if len(columns) != len(teamnames):
            logger.error("Data row length does not match header length")
            return json.dumps({"error": "Data row length mismatch"}), 500

        for i in range(1, len(teamnames)):
            print(teamnames[i])
            if teamnames[i].strip() == "":
                continue
            (teamnum, teamname) = teamnames[i].split(" ", 1)
            if int(teamnum) not in result:
                result[int(teamnum)] = {"teamnum": teamnum, "teamname": teamname}

            result[int(teamnum)][columns[0]] = columns[i]

    return json.dumps(
        result
    )


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
