# Import necessary libraries and modules
from flask import Flask, render_template, request, flash, redirect, url_for
import mysql.connector
from datetime import datetime
import secrets
from connect import create_db_connection, close_db_connection


# database connection and check if it's successful
connection = create_db_connection()
if connection:
    print("Connected to the database successfully.")
    close_db_connection(connection)

# secret key for the Flask app
secret_key = secrets.token_hex(24)

# Flask app instance
app = Flask(__name__, static_url_path='/static')
app.secret_key = secret_key

# Define routes

# Home page
@app.route("/")
def home():
    return render_template("base.html")

# List drivers
@app.route("/listdrivers")
def listdrivers():
    connection = create_db_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM driver ORDER BY surname, first_name;"
    cursor.execute(query)
    driver_list = cursor.fetchall()
    close_db_connection(connection)
    return render_template("driverlist.html", driver_list=driver_list)

# List courses
@app.route("/listcourses")
def listcourses():
    connection = create_db_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM course;"
    cursor.execute(query)
    course_list = cursor.fetchall()
    close_db_connection(connection)
    return render_template("courselist.html", course_list=course_list)


# Function to fetch a driver's runs from the database
@app.route('/driverdetails', methods=['GET', 'POST'])
def driver_details():
    if request.method == 'GET':
        drivers = get_drivers()
        return render_template('driver_details.html', drivers=drivers, driver_data=None, get_total_runs=get_total_runs)

    if request.method == 'POST':
        driver_id = request.form.get('driver_id')
        driver_data = get_driver_details(driver_id)  # Ensure it returns a list of dictionaries
        drivers = get_drivers()

        return render_template('driver_details.html', drivers=drivers, driver_data=driver_data, get_total_runs=get_total_runs)

@app.route('/driver/<int:driver_id>')
def driver_details_by_id(driver_id):
    driver_data = get_driver_details(driver_id)
    total_runs = get_total_runs(driver_id)  # Calculate total runs
    return render_template('driver_details.html', driver_data=driver_data, get_total_runs=get_total_runs)

# Function to fetch a course's runs from the database
def get_total_runs(driver_id):
    connection = create_db_connection()
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM run WHERE dr_id = %s"
    cursor.execute(query, (driver_id,))
    total_runs = cursor.fetchone()[0]
    close_db_connection(connection)
    return total_runs

def get_driver_details(driver_id):
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT driver.driver_id, driver.first_name, driver.surname, car.model, car.drive_class, 
            run.run_num, run.seconds, run.cones, course.name
        FROM driver
        JOIN car ON driver.car = car.car_num
        JOIN run ON driver.driver_id = run.dr_id
        JOIN course ON run.crs_id = course.course_id
        WHERE driver.driver_id = %s;
    """
    cursor.execute(query, (driver_id,))
    driver_data = cursor.fetchall()
    close_db_connection(connection)
    return driver_data

def get_drivers():
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM driver")
    drivers = cursor.fetchall()
    close_db_connection(connection)
    return drivers

# Edit Runs page
# Function to get runs from the database based on the selection
@app.route('/editruns', methods=['GET', 'POST'])
def edit_runs():
    if request.method == 'GET':
        drivers = get_drivers()
        courses = get_courses()
        runs = []
        return render_template('editruns.html', drivers=drivers, courses=courses, runs=runs)

    if request.method == 'POST':
        driver_id = request.form.get('driver_id')
        course_id = request.form.get('course_id')
        runs = []

        if driver_id:
            runs = get_runs("driver", driver_id)
        elif course_id:
            runs = get_runs("course", course_id)

        drivers = get_drivers()
        courses = get_courses()

        return render_template('editruns.html', drivers=drivers, courses=courses, runs=runs)

@app.route('/editruns/update', methods=['POST'])
def update_runs():
    edited_runs = request.form.getlist('editedruns')
    driver_id = request.form.get('driver_id')
    for run_id in edited_runs:
        run_time = request.form.get(f'run_time_{run_id}')
        cones = request.form.get(f'cones_{run_id}')
        wd = request.form.get(f'wd_{run_id}')
        update_run_in_database(run_id, run_time, cones, wd)
    flash("Runs updated successfully!", "success")
    return redirect(url_for('edit_runs'))

def get_runs(selection_type, selected_id):
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    if selection_type == "driver":
        cursor.execute("SELECT run_num, seconds, cones, wd FROM run WHERE dr_id = %s", (selected_id,))
    elif selection_type == "course":
        cursor.execute("SELECT run_num, seconds, cones, wd FROM run WHERE crs_id = %s", (selected_id,))
    runs = cursor.fetchall()
    close_db_connection(connection)
    return runs

def get_drivers():
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT driver_id, first_name, surname FROM driver")
    drivers = cursor.fetchall()
    close_db_connection(connection)
    return drivers

def get_courses():
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT course_id, name FROM course")
    courses = cursor.fetchall()
    close_db_connection(connection)
    return courses

def update_run_in_database(run_id, run_time=None, cones=None, wd=None):
    try:
        connection = create_db_connection()
        cursor = connection.cursor()
        update_query = "UPDATE run SET "
        params = []
        
        if run_time is not None:
            update_query += "seconds = %s, "
            params.append(run_time)
        if cones is not None:
            update_query += "cones = %s, "
            params.append(cones)
        if wd is not None:
            update_query += "wd = %s, "
            params.append(wd)

        # Remove the trailing comma and add the WHERE condition
        update_query = update_query.rstrip(", ") + " WHERE run_num = %s;"
        params.append(run_id)

        cursor.execute(update_query, tuple(params))
        connection.commit()
        flash("Run data updated successfully!", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    finally:
        close_db_connection(connection)



# Run list page
# Define the list_runs function
def list_runs():
    try:
        connection = create_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM run')
            runs = cursor.fetchall()
            connection.close()
            return runs
        return []
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return []
    
@app.route('/runs')
def display_runs():
    runs = list_runs()
    return render_template('run_list.html', runs=runs)

# Add driver page
@app.route("/adddriver", methods=["GET", "POST"])
def add_driver():
    if request.method == "GET":
        connection = create_db_connection()
        cursor = connection.cursor()
        fetch_car_query = "SELECT car_num, model FROM car"
        cursor.execute(fetch_car_query)
        car_options = cursor.fetchall()
        fetch_caregiver_query = "SELECT driver_id, CONCAT(first_name, ' ', surname) FROM driver WHERE caregiver IS NULL"
        cursor.execute(fetch_caregiver_query)
        caregiver_options = cursor.fetchall()
        close_db_connection(connection)
        return render_template("adddriver.html", car_options=car_options, caregiver_options=caregiver_options)

    if request.method == "POST":
        first_name = request.form.get("first_name")
        surname = request.form.get("surname")
        is_junior = int(request.form.get("is_junior")) if request.form.get("is_junior") else 0
        date_of_birth = request.form.get("date_of_birth") if is_junior else None
        car = int(request.form.get("car")) if request.form.get("car") is not None else None
        caregiver = int(request.form.get("caregiver")) if is_junior and request.form.get("caregiver") is not None else None
        age = None
        
        if is_junior and date_of_birth:
            dob = datetime.strptime(date_of_birth, "%Y-%m-%d")
            today = datetime.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        if is_junior is not None and is_junior != "":
            is_junior = int(is_junior)
        
        connection = create_db_connection()
        cursor = connection.cursor()
        # Insert the new driver
        insert_driver_query = "INSERT INTO driver (first_name, surname, date_of_birth, age, caregiver, car, is_junior) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_driver_query, (first_name, surname, date_of_birth, age, caregiver, car, is_junior))
        connection.commit()  # Commit the driver insertion

        # Get the driver_id of the newly added driver
        driver_id = cursor.lastrowid

        # Insert 12 blank runs for the new driver
        for course_id in ["A", "B", "C", "D", "E", "F"]:
            for run_num in range(1, 3):
                insert_run_query = "INSERT INTO run (dr_id, crs_id, run_num, seconds, cones, wd) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(insert_run_query, (driver_id, course_id, run_num, None, None, 0))
        connection.commit()

        close_db_connection(connection)
        flash("Driver added successfully!", "success")
        return redirect(url_for("listdrivers"))

# Search drivers page
@app.route("/searchdrivers", methods=["GET", "POST"])
def search_drivers():
    if request.method == "POST":
        driver_name = request.form.get("driver_name")
        if driver_name:
            connection = create_db_connection()
            cursor = connection.cursor()
            query = "SELECT * FROM driver WHERE first_name COLLATE utf8mb4_general_ci LIKE %s"
            params = ('%' + driver_name + '%',)  # Adjust the query for partial text match
            cursor.execute(query, params)
            result = cursor.fetchall()
            close_db_connection(connection)
            if result:
                return render_template("searchresult.html", driver_name=driver_name, driver_details=result)
            else:
                flash("Driver not found.")
        else:
            flash("Please enter a driver name.")
    return render_template("driversearch.html", available_names=get_available_names())

# Function to get available driver names from the database
def get_available_names():
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT first_name FROM driver")
    first_names = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT DISTINCT surname FROM driver")
    surnames = [row[0] for row in cursor.fetchall()]
    close_db_connection(connection)
    available_names = list(set(first_names))
    return available_names


# Junior Driver page
@app.route('/juniordrivers')
def junior_drivers():
    try:
        connection = create_db_connection()
        cursor = connection.cursor()

        query = """
            SELECT d1.first_name, d1.surname, d1.age, d2.first_name AS caregiver_name
            FROM driver AS d1
            LEFT JOIN driver AS d2 ON d1.caregiver = d2.driver_id
            WHERE d1.is_junior = 1
            ORDER BY d1.age DESC, d1.surname;
        """

        cursor.execute(query)

        results = cursor.fetchall()

        return render_template('juniordrivers.html', junior_drivers=results)

    except Exception as e:
        return f"An error occurred: {str(e)}"

    finally:
        close_db_connection(connection)

# Helper functions for database operations and queries
# Function to get car options from the database
def get_caregiver_options():
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT driver_id, CONCAT(first_name, ' ', surname) FROM driver WHERE caregiver IS NOT NULL"
        cursor.execute(query)
        caregiver_options = cursor.fetchall()
        cursor.close()
        connection.close()
        return caregiver_options
    return {'error': 'Database connection error'}

# Function to get car options from the database
def get_car_options():
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT car_id, car_name FROM car"
        cursor.execute(query)
        car_options = cursor.fetchall()
        cursor.close()
        connection.close()
        return car_options
    return {'error': 'Database connection error'}

# Function to retrieve data from the database
def get_data_from_database(table_name):
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data
    return {'error': 'Database connection error'}

# Function to get drivers from the database
def get_drivers_from_database():
    return get_data_from_database('driver')

# Function to get courses from the database
def get_courses_from_database():
    return get_data_from_database('course')


def fetch_results_from_database():
    try:
        connection = create_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)

            # Fetch course names from the database
            cursor.execute("SELECT DISTINCT name FROM course")
            course_names = [row['name'] for row in cursor.fetchall()]

            # Create a results dictionary with course times initialized to 0
            results = {}

            # Execute a SQL query to retrieve results
            query = """
            SELECT
                CONCAT(d.first_name, ' ', d.surname) AS driver_name,
                c.model AS car_model,
                dr.age AS age,
                cr.name AS course_name,
                r.seconds AS course_seconds
            FROM run AS r
            JOIN driver AS d ON r.dr_id = d.driver_id
            JOIN car AS c ON d.car = c.car_num
            JOIN driver AS dr ON r.dr_id = dr.driver_id
            JOIN course AS cr ON r.crs_id = cr.course_id
            WHERE r.seconds IS NOT NULL
            ORDER BY driver_name, course_name
            """

            cursor.execute(query)

            for row in cursor.fetchall():
                driver_name = row['driver_name']
                car_model = row['car_model']
                age = row['age']
                course_name = row['course_name']
                course_seconds = row['course_seconds']

                if driver_name not in results:
                    results[driver_name] = {
                        'car_model': car_model,
                        'age': age,
                        'course_times': {name: 0 for name in course_names}
                    }

                results[driver_name]['course_times'][course_name] = course_seconds

            close_db_connection(connection)
            return results
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None

# Function to determine the winner
def determine_winner(results):
    winner = None
    best_time = float('inf')

    for driver_name, data in results.items():
        total_time = sum(data['course_times'].values())
        if total_time < best_time:
            best_time = total_time
            winner = driver_name

    return winner


# Function to get the sorted list of drivers based on total time

def get_sorted_results(results):
    sorted_results = sorted(results.items(), key=lambda driver: sum(driver[1]['course_times'].values()))
    return sorted_results


def get_top_4_drivers(results, winner):
    top_4_drivers = []
    count = 0

    for driver_name, data in sorted(results.items(), key=lambda x: sum(x[1]['course_times'].values())):
        if driver_name == winner:
            continue
        if count < 4:
            top_4_drivers.append({'name': driver_name, 'data': data})
            count += 1
    return top_4_drivers

# Import the necessary libraries for plotting the graph
import plotly.express as px
import pandas as pd


# Define a route for overall results
@app.route('/overall_results')
def overall_results():
    # Fetch the results from the database using your logic
    results = fetch_results_from_database()
    winner = determine_winner(results)
    sorted_results = sorted(results.items(), key=lambda driver: sum(driver[1]['course_times'].values()))

    top_4_drivers = sorted_results[:5]  # Get the top 5 drivers
    nq_drivers = [driver for driver in sorted_results if driver[0] != winner and driver not in top_4_drivers]

    return render_template('overall_results.html', results=sorted_results, winner=winner, top_4_drivers=top_4_drivers, nq_drivers=nq_drivers)

# Define a route for the top 5 drivers graph
# Define a route for the top 5 drivers graph
@app.route('/top5graph')
def top5graph():
    # Fetch the results from the database using your logic
    results = fetch_results_from_database()
    sorted_results = get_sorted_results(results)
    top5_drivers = sorted_results[:5]
    
    # Sort the top 5 drivers in reverse order based on their total run times
    top5_drivers = sorted(sorted_results[:5], key=lambda driver: sum(driver[1]['course_times'].values()), reverse=True)

    driver_names = [driver[0] for driver in top5_drivers]
    overall_results = [sum(driver[1]['course_times'].values()) for driver in top5_drivers]

    # Render the 'top5graph.html' template with the graph data
    return render_template('top5graph.html', driver_names=driver_names, overall_results=overall_results)
# User - Admin page
@app.route('/admin')
def admin():
    return render_template('admin.html')

# Run the Flask app if this script is executed
if __name__ == "__main__":
    app.run(debug=True)
