from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    if os.getenv('TESTING'):
        return os.getenv('TESTING')
    else:
        return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'
