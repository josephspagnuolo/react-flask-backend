from flask import Flask, jsonify
from flask_cors import CORS
import os
import pymysql

app = Flask(__name__)
cors = CORS(app, origins='*')

timeout = 10
connection = pymysql.connect(
    charset="utf8mb4",
    connect_timeout=timeout,
    cursorclass=pymysql.cursors.DictCursor,
    db="defaultdb",
    host=os.getenv('HOST'),
    password=os.getenv('PASSWORD'),
    read_timeout=timeout,
    port=16562,
    user="avnadmin",
    write_timeout=timeout,
)

def doDB():
    result = []
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS mytest (id INTEGER PRIMARY KEY)")
        cursor.execute("INSERT INTO mytest (id) VALUES (1), (2)")
        cursor.execute("SELECT * FROM mytest")
        result = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()
    return result

@app.route('/')
def home():
    if os.getenv('TESTING'):
        result = doDB()
        return jsonify(
            {
                "testing": {
                    "env": testing_env,
                    "db_result": result
                }
            }
        )
    else:
        return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'
