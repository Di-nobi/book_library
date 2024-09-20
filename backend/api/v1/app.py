#!/bin/bash python3
from flask import Flask, jsonify
from flask_cors import CORS
from database import storage
from api.v1.views import app_look
app = Flask(__name__)


app.register_blueprint(app_look)
CORS(app)
@app.teardown_appcontext
def closeDB(e=None):
    storage.close_session()


@app.errorhandler(404)
def notFound(err):
    return jsonify({'error': f'Not found {err}'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)