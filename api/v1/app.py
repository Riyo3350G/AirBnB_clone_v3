#!/usr/bin/python3
"""flask app"""
from flask import Flask
from os import getenv
from models import storage
from api.v1.views import app_views


app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(self):
    """teardown"""
    storage.close()


if __name__ == "__main__":
    if getenv('HBNB_API_HOST') is None:
        host = '0.0.0.0'
    else:
        host = getenv('HBNB_API_HOST')

    if getenv('HBNB_API_PORT') is None:
        port = '5000'
    else:
        port = getenv('HBNB_API_PORT')
    app.run(host=host, port=port, threaded=True)
