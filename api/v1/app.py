#!/usr/bin/python3
"""
This module contains the main application for the API.

The API is designed to provide endpoints for managing resources.
It uses Flask to handle HTTP requests and integrates with a storage
system to manage data persistence.

"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception=None):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def error_nof(error):
    """ return 404 when a resource was not foud """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    """ main flask app"""
    import os
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
