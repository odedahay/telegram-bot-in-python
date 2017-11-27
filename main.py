import logging
import json

from flask import Flask
from flask import request

from demobot import get_last_id_text

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def hello():
    """Return a friendly HTTP greeting."""
    print("Test!")
    req = request.data.decode("utf-8")
    update = json.loads(req)
    get_last_id_text(update)
    return ''


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8000, debug=True)
# [END app]
