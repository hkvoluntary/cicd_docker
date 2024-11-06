from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

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
            print('Connection to MySQL successful')
    except Error as e:
        print(f"Error: '{e}'")
    return connection

# Create route to add a new record
@app.route('/create', methods=['POST'])
def create_record():
    connection = create_connection()
    cursor = connection.cursor()

    # Get data from POST request body
    data = request.get_json()

    # Extract data from JSON
    name = data.get('name')
    age = data.get('age')

    # Insert the record into the MySQL table
    try:
        cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
        connection.commit()  # Commit the transaction
        response = {'message': 'Record added successfully!'}
    except Error as e:
        connection.rollback()  # Rollback in case of error
        response = {'message': f'Error: {e}'}

    cursor.close()
    connection.close()

    return jsonify(response)

# Read route to fetch all records
@app.route('/read', methods=['GET'])
def read_records():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users")
    records = cursor.fetchall()

    result = []
    for row in records:
        result.append({'id': row[0], 'name': row[1], 'age': row[2]})

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

    # Update the record in the MySQL table
    try:
        cursor.execute("UPDATE users SET name = %s, age = %s WHERE id = %s", (new_name, new_age, id))
        connection.commit()  # Commit the transaction
        if cursor.rowcount > 0:
            response = {'message': 'Record updated successfully!'}
        else:
            response = {'message': 'No record found with the provided ID'}
    except Error as e:
        connection.rollback()  # Rollback in case of error
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
            response = {'message': 'Record deleted successfully!'}
        else:
            response = {'message': 'No record found with the provided ID'}
    except Error as e:
        connection.rollback()  # Rollback in case of error
        response = {'message': f'Error: {e}'}

    cursor.close()
    connection.close()

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
