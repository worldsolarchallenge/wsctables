"""WSC Earth is a flask app which renders a map of the current car positions."""

import argparse
import logging
import os

from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix



config = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "FileSystemCache",  # Flask-Caching related configs
    "CACHE_DIR": os.environ.get("CACHE_DIR", "/tmp/wsctables_cache"),  # Directory for fs cache files
    "CACHE_DEFAULT_TIMEOUT": 300,
}

memcached_servers = os.environ.get("CACHE_MEMCACHED_SERVERS")
if memcached_servers:
    memcached_servers = memcached_servers.split(",")
    logging.info("Using Memcached cache servers: %s", memcached_servers)
    config["CACHE_TYPE"] = "MemcachedCache"
    config["CACHE_KEY_PREFIX"] = "wsctables_" # Prefix for cache keys
    config["CACHE_MEMCACHED_SERVERS"] = memcached_servers

app = Flask(__name__)

logging.info("Using cache type: %s", config["CACHE_TYPE"])

app.config.from_mapping(config)
app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1)
cache = Cache(app)
cors = CORS(app)

###########################
# Gather influx parameters.
###########################


app.config["INFLUX_TOKEN_TARGET"] = os.environ.get("INFLUX_TOKEN_TARGET", None)
app.config["CREDS_PATH"] = os.environ.get("CREDS_PATH", "credentials.json") # service account key
app.config["CONFIG_YAML"] = os.environ.get("CONFIG_YAML", "config.yaml")

import wsctables.views  # pylint: disable=wrong-import-position

def main():
    """Main function to run the Flask app."""
    parser = argparse.ArgumentParser()

    parser.add_argument("--port", default=5000)

    args = parser.parse_args()

    app.config.update(
        CONFIG_YAML=args.config,
        CREDSPATH=args.credspath,
        INFLUX_TOKEN_TARGET=args.influx_token_target
    )

    app.run(debug=True, host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    LOG_FORMAT = "%(asctime)s - %(module)s - %(levelname)s - Thread_name: %(threadName)s - %(message)s"
    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
    main()
