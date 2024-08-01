from flask import Flask, request, jsonify
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

def getDB():
    result = []
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM pledgx")
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

def insertDB(first_name, last_name, phone_number, job_title, country):
    result = []
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pledgx (
                id INTEGER AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                phone_number VARCHAR(20),
                job_title VARCHAR(255),
                country VARCHAR(255)
            )
        """)
        # Insert the data into the table
        cursor.execute("""
            INSERT INTO pledgx (first_name, last_name, phone_number, job_title, country)
            VALUES (%s, %s, %s, %s, %s)
        """, (first_name, last_name, phone_number, job_title, country))
        connection.commit()
        cursor.execute("SELECT * FROM pledgx")
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

@app.route('/', methods=['GET'])
def home():
    result = getDB()
    return jsonify({"result": result})

@app.route('/edit', methods=['POST'])
def edit():
    try:
        data = request.json
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        phone_number = data.get('phoneNumber')
        job_title = data.get('jobTitle')
        country = data.get('country')
        if not all([first_name, last_name, phone_number, job_title, country]):
            return jsonify({"error": "Missing data"}), 400
        
        result = insertDB(first_name, last_name, phone_number, job_title, country)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
