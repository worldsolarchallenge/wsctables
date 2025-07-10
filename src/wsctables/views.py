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
    """Render an index page"""
    data = ""
    for name in ["scrutineering", "judging", "laptimes", "penalties"]:
        data += f'<a href="{name}.html">{name.capitalize()}</a> | '
    return data


@app.route("/scripts/wsctables.js")
#@cache.cached()
def tables_script():
    """Templated wsctables.js to allow for base URL rendering"""
    return flask.render_template("wsctables.js.j2")

def get_table_data(url, teams_across=False, split_team_name=False, exclude=[]):
    """Fetch table data from the given URL."""

    r = requests.get(url, timeout=10)
    if r.status_code != 200:
        logger.error("Failed to fetch data from GitHub API: %s", r.status_code)
        return json.dumps({"error": "Failed to fetch data"}), 500

    # Parse the TSV data into a list of lines
    # Assuming the data is tab-separated values (TSV)

    teamdata = []

    header_txt = r.text.splitlines()[0]
    if not header_txt.strip():
        logger.error("No data found in the response header")
        return json.dumps({"error": "No data found"}), 500

    colnames = header_txt.split("\t")

    for line in r.text.splitlines()[1:]:
        if not line.strip():
            continue

        # Split the line into columns
        columns = line.split("\t")

        if len(columns) != len(colnames):
            logger.error("Data row length does not match header length")
            return json.dumps({"error": "Data row length mismatch"}), 500

        if teams_across:
            for i in range(1, len(colnames)):
                print(colnames[i])
                if colnames[i].strip() == "":
                    continue
                (teamnum, teamname) = colnames[i].split(" ", 1)

                if len(teamdata) < i:
                    teamdata.append({"Team": teamnum, "Name": teamname})

                if columns[0] not in exclude:
                    teamdata[i-1][columns[0]] = columns[i]
        else:
            entry = dict(zip(colnames, columns))
            if( entry.get("Team", "").strip() == "" ):
                continue

            entry_filtered = {key: value for key, value in entry.items()
                        if key not in exclude and key.strip() != ""}

            teamdata.append(entry_filtered)

    result = {"teamdata": teamdata}
    return json.dumps(
        result
    )

@app.route("/scripts/scrutineering.js")
#@cache.cached()
def scrutineering_script():
    """Templated wsctables.js to allow for base URL rendering"""
    return flask.render_template("scrutineering.js.j2")


@app.route("/api/scrutineering/")
#@cache.cached(timeout=30)
#@flask_cachecontrol.cache_for(seconds=30)
def scrutineering_data():
    """API Endpoint to fetch scrutineering data as JSON"""
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQfPSSyRC2uuklVHGwzWLzrsEPmYYmF9dQVeHzGZQKIiovsyHAuSWATx3IDlMbqVBD1Scnbldv8rm9I/pub?gid=0&single=true&output=tsv' # pylint: disable=line-too-long

    return get_table_data(url, teams_across=True, split_team_name=True)

@app.route("/scrutineering.html")
#@cache.cached(timeout=30)
#@flask_cachecontrol.cache_for(seconds=30)
def scrutineering():
    """Render a table"""
    return flask.render_template(
        "tables.html.j2",
        name="scrutineering",
        script_name="scrutineering")


@app.route("/api/judging/")
#@cache.cached(timeout=30)
#@flask_cachecontrol.cache_for(seconds=30)
def judging_data():
    """API Endpoint to fetch judging data as JSON"""
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSW1_kFF14mV0s7cx5DKpqCMnUQvGEtKv0J_xlFuG9Hg4KgdYKHFzcTAZncN3dYivgH3xANeP1wze0R/pub?gid=15742234&single=true&output=tsv' # pylint: disable=line-too-long

    return get_table_data(url)

@app.route("/judging.html")
#@cache.cached(timeout=30)
#@flask_cachecontrol.cache_for(seconds=30)
def judging():
    """Render a table"""
    return flask.render_template(
        "tables.html.j2",
        name="judging",
        script_name="wsctables")



@app.route("/api/laptimes/")
#@cache.cached(timeout=30)
#@flask_cachecontrol.cache_for(seconds=30)
def laptimes_data():
    """API Endpoint to fetch laptimes data as JSON"""
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vS45Yt9IN4RkHt_gPJP_JpV6gxHvXfOBIc4k46OT4eq1fNFfvynYeIuc3G1ZTtTIqbXd9sTgoGFc50W/pub?gid=2081640324&single=true&output=tsv' # pylint: disable=line-too-long

    return get_table_data(url, teams_across=False,
        exclude=["Lap time (s)", "Track Distance"])

@app.route("/laptimes.html")
#@cache.cached(timeout=30)
#@flask_cachecontrol.cache_for(seconds=30)
def laptimes():
    """Render a table"""
    return flask.render_template(
        "tables.html.j2",
        name="laptimes",
        script_name="wsctables",)



@app.route("/api/penalties/")
#@cache.cached(timeout=30)
#@flask_cachecontrol.cache_for(seconds=30)
def penalties_script():
    """API Endpoint to fetch penalties data as JSON"""
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vS45Yt9IN4RkHt_gPJP_JpV6gxHvXfOBIc4k46OT4eq1fNFfvynYeIuc3G1ZTtTIqbXd9sTgoGFc50W/pub?gid=662069405&single=true&output=tsv' # pylint: disable=line-too-long

    return get_table_data(url, teams_across=False)

@app.route("/penalties.html")
#@cache.cached(timeout=30)
#@flask_cachecontrol.cache_for(seconds=30)
def penalties():
    """Render a table"""
    return flask.render_template(
        "tables.html.j2",
        name="penalties",
        script_name="wsctables")
