from . import app
import mysql.connector
from flask import Flask, jsonify

# app = Flask(__name__)

# Replace with your database credentials
host = 'localhost'  # or '127.0.0.1'
port = 3306
user = 'sid'
password = '$Sidtheboss1'
database = 'movie_app'

# Create a database connection
conn = mysql.connector.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database
)

# Create a cursor to execute SQL queries
cursor = conn.cursor()

# Route to test the database connection
@app.route('/test_db_connection')
def test_db_connection():
    try:
        cursor.execute("SELECT * FROM movies LIMIT 1")
        data = cursor.fetchone()
        return jsonify({"message": "Database connection successful", "data": data})
    except Exception as e:
        return jsonify({"message": f"Database connection error: {str(e)}"})

# if __name__ == "__main__":
#     app.run(debug=True)
