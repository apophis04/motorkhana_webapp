# Import necessary libraries and modules
from flask import Flask, render_template, request
import mysql.connector
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

# Function to fetch results from the database
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

# Run the Flask app if this script is executed
if __name__ == "__main__":
    app.run(debug=True)
