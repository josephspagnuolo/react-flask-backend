from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
cors = CORS(app, origins='*')

@app.route('/')
def home():
    if os.getenv('TESTING'):
        return jsonify(
            { "testing":  os.getenv('TESTING') }
        )
    else:
        return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'
