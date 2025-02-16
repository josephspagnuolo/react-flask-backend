from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from supabase import create_client, Client
import os
import pymysql

app = Flask(__name__)
cors = CORS(app, origins=[os.getenv('FRONTEND_URL')])

supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)
bucket_name = 'fullstackdevassignment'

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
        cursor.execute("SELECT * FROM flask")
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

def insertDB(file_name, first_name, last_name, phone_number, job_title, country):
    result = []
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS flask")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS flask (
                id INTEGER AUTO_INCREMENT PRIMARY KEY,
                file_name VARCHAR(255),
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                phone_number VARCHAR(20),
                job_title VARCHAR(255),
                country VARCHAR(255)
            )
        """)
        # Insert the data into the table
        cursor.execute("""
            INSERT INTO flask (file_name, first_name, last_name, phone_number, job_title, country)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (file_name, first_name, last_name, phone_number, job_title, country))
        connection.commit()
        cursor.execute("SELECT * FROM flask")
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
        file = request.files.get('file')
        file_name = request.form.get('fileName')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        phone_number = request.form.get('phoneNumber')
        job_title = request.form.get('jobTitle')
        country = request.form.get('country')

        if file:
            supabase.storage.from_(bucket_name).remove([f'profile/{file_name}'])
            new_file_name = f'avatar{datetime.now().strftime("%Y%m%d%H%M%S")}.png'
            file_content = file.read()
            supabase.storage.from_(bucket_name).upload(f'profile/{new_file_name}', file_content, {
                'content-type': file.content_type
            })
            file_name = new_file_name
        
        result = insertDB(file_name, first_name, last_name, phone_number, job_title, country)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
