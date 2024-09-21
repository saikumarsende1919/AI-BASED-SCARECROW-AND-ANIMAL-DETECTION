from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
import subprocess
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a secret key for session management
@app.route("/")
def home():
    return render_template("login.html")
# MySQL Configuration
running_processes={}
db_config = {
    'host': 'localhost',
    'database': 'mini_pro',
    'user': 'root',
    'password': 'Sai@1919'  # Replace with your MySQL password
}

# Function to create a MySQL connection
def create_connection():
    connection = None
    try:
        # print("rrr")
        connection = mysql.connector.connect(**db_config)
        print("MySQL Database connection successful")
    except Error as e:
        print(f"Error: '{e}'")
    return connection

# Route for handling login
@app.route('/login', methods=['POST'])
def login():
    connection = create_connection()
    if connection is None:
        return "Database connection error"

    email = request.form['email']
    password = request.form['pswd']

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            # Store user session to track login status
            session['user'] = user[0]  # Assuming user[0] is the user_id or a unique identifier
            return redirect(url_for('dashboard'))
        else:
            return "Invalid email or password. Please try again."
    except Error as e:
        print(f"Error: '{e}'")
        return "Login failed. Please try again."

# Route for dashboard after successful login
@app.route('/dashboard')
def dashboard():
    # Check if user is logged in
    if 'user' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('home'))  # Redirect to login page if not logged in

@app.route('/stop_process')
def stop_proces():
    # Terminate the subprocess
    running_process = None
    for pid in running_processes:
        running_processes[pid]['process'].terminate()
                # Remove from global dictionary
        del running_processes[pid]
        break
    return render_template('dashboard.html')
# Route to run notebook file
@app.route('/run_notebook', methods=['POST'])
def run_notebook():
    global running_process
    if 'user' in session:
        try:
            running_process=subprocess.Popen(['python', 'temp.py'])
            running_processes[running_process.pid] = {
            'process': running_process,
            'status': 'running'
        }
            return render_template('dashboard.html')
        except subprocess.CalledProcessError as e:
            print(f"Error executing notebook: {e}")
            return "Notebook execution failed."
    else:
        return redirect(url_for('home'))  # Redirect to login page if not logged in

# Main method to run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
