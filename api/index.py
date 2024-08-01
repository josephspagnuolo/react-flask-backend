from flask import Flask, jsonify
from flask_cors import CORS
import os
import pymysql

app = Flask(__name__)
cors = CORS(app, origins='*')

def get_db_connection():
    return pymysql.connect(
        charset="utf8mb4",
        connect_timeout=10,
        cursorclass=pymysql.cursors.DictCursor,
        db="defaultdb",
        host=os.getenv('HOST'),
        password=os.getenv('PASSWORD'),
        read_timeout=10,
        port=16562,
        user="avnadmin",
        write_timeout=10,
    )

def doDB():
    result = []
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS mytest (id INTEGER PRIMARY KEY)")
        cursor.execute("INSERT INTO mytest (id) VALUES (1), (2)")
        cursor.execute("SELECT * FROM mytest")
        result = cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"MySQL error: {e}")
        result = {"error": str(e)}
    except Exception as e:
        print(f"Error: {e}")
        result = {"error": str(e)}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    return result

@app.route('/')
def home():
    if os.getenv('TESTING'):
        result = doDB()
        return jsonify(
            {
                "testing": {
                    "env": os.getenv('TESTING'),
                    "db_result": result
                }
            }
        )
    else:
        return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'
