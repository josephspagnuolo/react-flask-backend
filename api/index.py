from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
cors = CORS(app, origins='*')

def math(number1, number2):
    return number1 + number2

@app.route('/')
def home():
    if os.getenv('TESTING'):
        result = math(3, 4)
        return jsonify(
            {
                "testing": {
                    os.getenv('TESTING'),
                    result
                }
            }
        )
    else:
        return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'
