from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import logging

app = Flask(__name__)

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG,  # Log level (DEBUG will log all messages)
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    handlers=[logging.StreamHandler()])  # Logs to console

# MySQL connection configuration
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='172.17.0.3',   # MySQL host (e.g., 'localhost' or Docker container name)
            user='sql',  # MySQL username
            password='sql1245',  # MySQL password
            database='test_db'  # Database name
        )
        if connection.is_connected():
            logging.info('Connection to MySQL successful')
    except Error as e:
        logging.error(f"Error connecting to MySQL: '{e}'")
    return connection

# Create route to add a new record with HKID check
@app.route('/create', methods=['POST'])
def create_record():
    connection = create_connection()
    cursor = connection.cursor()

    # Get data from POST request body
    data = request.get_json()

    # Extract data from JSON
    name = data.get('name')
    age = data.get('age')
    hkd_id = data.get('hkd_id')

    # Step 1: Check if the HKID already exists in the database
    try:
        cursor.execute("SELECT COUNT(*) FROM users WHERE hkd_id = %s", (hkd_id,))
        result = cursor.fetchone()
        if result[0] > 0:
            # If HKID exists, log an error and return an error response
            logging.warning(f"Duplicate HKID detected: {hkd_id}. Cannot insert record.")
            response = {'message': 'Error: HKID already exists. Cannot insert duplicate HKID.'}
        else:
            # Step 2: If HKID is unique, insert the new record
            cursor.execute("INSERT INTO users (name, age, hkd_id) VALUES (%s, %s, %s)", (name, age, hkd_id))
            connection.commit()  # Commit the transaction
            logging.info(f"Record added successfully: {name}, {age}, {hkd_id}")
            response = {'message': 'Record added successfully!'}
    except Error as e:
        connection.rollback()  # Rollback in case of error
        logging.error(f"Error during record insertion: {e}")
        response = {'message': f'Error: {e}'}

    cursor.close()
    connection.close()

    return jsonify(response)

# Read route to fetch all records
@app.route('/read', methods=['GET'])
def read_records():
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM users")
        records = cursor.fetchall()

        result = []
        for row in records:
            result.append({'id': row[0], 'name': row[1], 'age': row[2], 'hkd_id': row[3]})

        logging.info(f"Retrieved {len(result)} records from the database.")
    except Error as e:
        logging.error(f"Error during reading records: {e}")
        result = []

    cursor.close()
    connection.close()

    return jsonify(result)

# Update route to modify an existing record
@app.route('/update/<int:id>', methods=['PUT'])
def update_record(id):
    connection = create_connection()
    cursor = connection.cursor()

    # Get data from PUT request body
    data = request.get_json()
    new_name = data.get('name')
    new_age = data.get('age')
    new_hkd_id = data.get('hkd_id')

    # Update the record in the MySQL table
    try:
        cursor.execute("UPDATE users SET name = %s, age = %s, hkd_id = %s WHERE id = %s", (new_name, new_age, new_hkd_id, id))
        connection.commit()  # Commit the transaction
        if cursor.rowcount > 0:
            logging.info(f"Record with ID {id} updated successfully.")
            response = {'message': 'Record updated successfully!'}
        else:
            logging.warning(f"No record found with ID {id} for update.")
            response = {'message': 'No record found with the provided ID'}
    except Error as e:
        connection.rollback()  # Rollback in case of error
        logging.error(f"Error during record update: {e}")
        response = {'message': f'Error: {e}'}

    cursor.close()
    connection.close()

    return jsonify(response)

# Delete route to remove a record
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_record(id):
    connection = create_connection()
    cursor = connection.cursor()

    # Delete the record from the MySQL table
    try:
        cursor.execute("DELETE FROM users WHERE id = %s", (id,))
        connection.commit()  # Commit the transaction
        if cursor.rowcount > 0:
            logging.info(f"Record with ID {id} deleted successfully.")
            response = {'message': 'Record deleted successfully!'}
        else:
            logging.warning(f"No record found with ID {id} to delete.")
            response = {'message': 'No record found with the provided ID'}
    except Error as e:
        connection.rollback()  # Rollback in case of error
        logging.error(f"Error during record deletion: {e}")
        response = {'message': f'Error: {e}'}

    cursor.close()
    connection.close()

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
