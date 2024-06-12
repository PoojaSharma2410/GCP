# Import necessary modules
from flask import Flask, request, jsonify, render_template_string
import os
import psycopg2

# Initialize Flask app
app = Flask(__name__)

# Get the backend service IP address from environment variable
backend_service_ip = os.getenv("BACKEND_SERVICE_IP")

# Database connection setup
DATABASE_URL = (
    f"dbname='{os.getenv('DB_NAME', 'myappdb')}' "
    f"user='{os.getenv('DB_USER', 'myuser')}' "
    f"password='{os.getenv('DB_PASSWORD', 'mypassword')}' "
    f"host='{os.getenv('DB_HOST', '34.28.154.231')}'"
)

# Function to establish database connection
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Function to create the table if it does not exist
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# Create a new record in the database
@app.route('/create-record', methods=['POST'])
def create_record():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Get data from request
    data = request.form
    # Insert data into database
    cursor.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (data['username'], data['email']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Record created successfully'})

# Read records from the database
@app.route('/read-records', methods=['GET'])
def read_records():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    # Format records as JSON
    result = [{'id': record[0], 'username': record[1], 'email': record[2]} for record in records]
    return jsonify(result)

# Update a record in the database
@app.route('/update-record/<int:id>', methods=['PUT'])
def update_record(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Get data from request
    data = request.form
    # Update record in database
    cursor.execute("UPDATE users SET username = %s, email = %s WHERE id = %s", (data['username'], data['email'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Record updated successfully'})

# Delete a record from the database
@app.route('/delete-record/<int:id>', methods=['DELETE'])
def delete_record(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Delete record from database
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Record deleted successfully'})

# Define a route to display the HTML form
@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Web Application</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <form id="dataForm">
            <label for="value1">ID:</label>
            <input type="text" id="id" name="id" required>
            <label for="value1">Username:</label>
            <input type="text" id="username" name="username" required>
            <label for="value2">Email:</label>
            <input type="text" id="email" name="email" required>
            <button type="submit">Submit</button>
        </form>
        <script src="script.js"></script>
    </body>
    </html>
    ''')

# Run the Flask app
if __name__ == '__main__':
    create_table()  # Ensure the table is created when the application starts
    app.run(host='0.0.0.0', port=80, debug=True)
