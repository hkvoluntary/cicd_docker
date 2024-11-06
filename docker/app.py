from flask import Flask
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL connection configuration
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='172.17.0.3',   # Host where MySQL is running (e.g., 'localhost' or Docker container name)
            user='sql',  # Your MySQL username
            password='sql1245',  # Your MySQL password
            database='test_db'  # The database you want to connect to
        )
        if connection.is_connected():
            print('Connection to MySQL successful')
    except Error as e:
        print(f"Error: '{e}'")
    return connection

@app.route('/')
def hello_world():
    # Connect to the MySQL database
    connection = create_connection()
    cursor = connection.cursor()

    # Example query (make sure you have a table and some data in the DB)
    cursor.execute("SELECT * FROM users LIMIT 1")
    result = cursor.fetchone()  # Fetch one record

    # Return data from MySQL as part of the response
    if result:
        message = f"Hello, Docker World! First record from MySQL: {result}"
    else:
        message = "Hello, Docker World! No data found in MySQL."

    # Close the connection
    cursor.close()
    connection.close()

    return message

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
