# Import necessary libraries and modules
from flask import Flask, render_template, request, flash, redirect, url_for
import mysql.connector
from datetime import datetime
import secrets
from connect import create_db_connection, close_db_connection
import functions

# Create a Flask app instance
app = Flask(__name__, static_url_path='/static')

# Define the secret key for the Flask app
secret_key = secrets.token_hex(24)
app.secret_key = secret_key

# Database connection and check if it's successful
connection = create_db_connection()
if connection:
    print("Connected to the database successfully.")
    close_db_connection(connection)

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
        drivers = functions.get_drivers()
        return render_template('driver_details.html', drivers=drivers, driver_data=None, get_total_runs=functions.get_total_runs)

    if request.method == 'POST':
        driver_id = request.form.get('driver_id')
        driver_data = functions.get_driver_details(driver_id)  # Ensure it returns a list of dictionaries
        drivers = functions.get_drivers()

        return render_template('driver_details.html', drivers=drivers, driver_data=driver_data, get_total_runs=functions.get_total_runs)

@app.route('/driver/<int:driver_id>')
def driver_details_by_id(driver_id):
    driver_data = functions.get_driver_details(driver_id)
    total_runs = functions.get_total_runs(driver_id)  # Calculate total runs
    return render_template('driver_details.html', driver_data=driver_data, get_total_runs=functions.get_total_runs)

# Edit Runs page
# Function to get runs from the database based on the selection
@app.route('/editruns', methods=['GET', 'POST'])
def edit_runs():
    if request.method == 'GET':
        drivers = functions.get_drivers()
        courses = functions.get_courses()
        runs = []
        return render_template('editruns.html', drivers=drivers, courses=courses, runs=runs)

    if request.method == 'POST':
        driver_id = request.form.get('driver_id')
        course_id = request.form.get('course_id')
        runs = []

        if driver_id:
            runs = functions.get_runs("driver", driver_id)
        elif course_id:
            runs = functions.get_runs("course", course_id)

        drivers = functions.get_drivers()
        courses = functions.get_courses()

        return render_template('editruns.html', drivers=drivers, courses=courses, runs=runs)

@app.route('/editruns/update', methods=['POST'])
def update_runs():
    edited_runs = request.form.getlist('editedruns')
    driver_id = request.form.get('driver_id')
    for run_id in edited_runs:
        run_time = request.form.get(f'run_time_{run_id}')
        cones = request.form.get(f'cones_{run_id}')
        wd = request.form.get(f'wd_{run_id}')
        functions.update_run_in_database(run_id, run_time, cones, wd)
    flash("Runs updated successfully!", "success")
    return redirect(url_for('edit_runs'))

# Run list page
@app.route('/runs')
def display_runs():
    runs = functions.list_runs()
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
    return render_template("driversearch.html", available_names=functions.get_available_names())

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

# Define routes for overall results and top 5 drivers graph
# Import the necessary libraries for plotting the graph
import plotly.express as px
import pandas as pd

# Define a route for overall results
@app.route('/overall_results')
def overall_results():
    # Fetch the results from the database using your logic
    results = functions.fetch_results_from_database()
    winner = functions.determine_winner(results)
    sorted_results = sorted(results.items(), key=lambda driver: sum(driver[1]['course_times'].values()))

    top_4_drivers = sorted_results[:5]  # Get the top 5 drivers
    nq_drivers = [driver for driver in sorted_results if driver[0] != winner and driver not in top_4_drivers]

    return render_template('overall_results.html', results=sorted_results, winner=winner, top_4_drivers=top_4_drivers, nq_drivers=nq_drivers)

# Define a route for the top 5 drivers graph
@app.route('/top5graph')
def top5graph():
    # Fetch the results from the database using your logic
    results = functions.fetch_results_from_database()
    sorted_results = functions.get_sorted_results(results)
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
