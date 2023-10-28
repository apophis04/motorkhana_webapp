import app

# Function to get the total runs for a driver
def get_total_runs(driver_id):
    connection = app.create_db_connection()
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM run WHERE dr_id = %s"
    cursor.execute(query, (driver_id,))
    total_runs = cursor.fetchone()[0]
    app.close_db_connection(connection)
    return total_runs

# Function to get detailed information about a driver
def get_driver_details(driver_id):
    connection = app.create_db_connection()
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
    app.close_db_connection(connection)
    return driver_data

# Function to get a list of drivers
def get_drivers():
    connection = app.create_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM driver")
    drivers = cursor.fetchall()
    app.close_db_connection(connection)
    return drivers

# Function to get a list of courses
def get_courses():
    connection = app.create_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT course_id, name FROM course")
    courses = cursor.fetchall()
    app.close_db_connection(connection)
    return courses

# Function to get runs for a specific driver or course
def get_runs(selection_type, selected_id):
    connection = app.create_db_connection()
    cursor = connection.cursor(dictionary=True)
    if selection_type == "driver":
        cursor.execute("SELECT run_num, seconds, cones, wd FROM run WHERE dr_id = %s", (selected_id,))
    elif selection_type == "course":
        cursor.execute("SELECT run_num, seconds, cones, wd FROM run WHERE crs_id = %s", (selected_id,))
    runs = cursor.fetchall()
    app.close_db_connection(connection)
    return runs

# Function to update a run in the database
def update_run_in_database(run_id, run_time=None, cones=None, wd=None):
    try:
        connection = app.create_db_connection()
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
        app.flash("Run data updated successfully!", "success")
    except Exception as e:
        app.flash(f"Error: {e}", "danger")
    finally:
        app.close_db_connection(connection)

# Function to list all runs
def list_runs():
    try:
        connection = app.create_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM run')
            runs = cursor.fetchall()
            connection.close()
            return runs
        return []
    except Exception as e:
        app.flash(f"An error occurred: {str(e)}", "error")
        return []

# Function to get available driver names from the database
def get_available_names():
    connection = app.create_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT first_name FROM driver")
    first_names = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT DISTINCT surname FROM driver")
    surnames = [row[0] for row in cursor.fetchall()]
    app.close_db_connection(connection)
    available_names = list(set(first_names))
    return available_names

# Function to get caregiver options
def get_caregiver_options():
    connection = app.create_db_connection()
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
    connection = app.create_db_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT car_id, car_name FROM car"
        cursor.execute(query)
        car_options = cursor.fetchall()
        cursor.close()
        connection.close()
        return car_options
    return {'error': 'Database connection error'}

# Function to retrieve data from the database for a specific table
def get_data_from_database(table_name):
    connection = app.create_db_connection()
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

# Function to fetch results from the database
def fetch_results_from_database():
    try:
        connection = app.create_db_connection()
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

            app.close_db_connection(connection)
            return results
    except app.mysql.connector.Error as e:
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

# Function to get the top 4 drivers based on total time
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
