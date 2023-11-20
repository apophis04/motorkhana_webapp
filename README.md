# Motorkhana Web Application

**Support My Work**

Hey there! 👋

I'm an independent creator working on various projects, from open-source software to content creation. If you find my work useful or enjoy what I do, consider supporting me with a virtual coffee!
Your support helps keep me fueled and motivated to continue creating and sharing. It's a small gesture that goes a long way in making a difference.

Thank you for being a part of my journey! ☕


--> [**Buy Me a Coffee ☕**](https://www.buymeacoffee.com/apophis04)


## Web Application Structure
### Routes
- **Home Page ("/")**
  - Renders the base template.
  
- **List Drivers ("/listdrivers")**
  - Retrieves and displays driver information.

- **List Courses ("/listcourses")**
  - Retrieves and displays course information.

- **Driver Details ("/driver/")**
  - Accepts GET and POST requests.
  - GET: Displays form to select a driver.
  - POST: Displays details of the selected driver.

- **Edit Runs ("/editruns")**
  - Accepts GET and POST requests.
  - GET: Displays form to select driver or course to edit runs.
  - POST: Displays runs of the selected driver or course for editing.

- **Update Runs ("/editruns/update")**
  - Route to update runs for a driver.
  - POST: Updates runs in the database.

- **Run List ("/runs")**
  - Displays a list of runs.

- **Add Driver ("/adddriver")**
  - Accepts GET and POST requests.
  - GET: Displays form to add a new driver.
  - POST: Handles form submission and data insertion into the database.

- **Search Driver ("/searchers")**
  - Accepts GET and POST requests.
  - GET: Displays form for searching drivers.
  - POST: Searches driver based on user input and displays results.

- **Junior Driver ("/juniordriver")**
  - Displays a list of junior drivers and their categories.

- **Over-all Results ("/overall_result")**
  - Displays overall results and determines the winner.

- **Top 5 Driver Graph ("/top5graph")**
  - Shows the top 5 drivers based on total run times.

- **Admin ("/admin")**
  - Route for the admin page.

### Functions
- **get_total_runs(driver_id):**
  - Retrieves the total number of runs for a specific driver.

- **get_driver_details(driver_id):**
  - Fetches detailed information about a specific driver, including their runs and associated data.

- **get_drivers():**
  - Retrieves a list of all drivers from the database.

- **get_courses():**
  - Retrieves a list of all courses from the database.

- **get_runs(selection_type, selected_id):**
  - Retrieves runs for a specific driver or course based on the selection type.

- **update_run_in_database(run_id, run_time, cones, wd):**
  - Updates data for a specific run in the database.

- **list_runs():**
  - Retrieves a list of all runs from the database.

- **get_available_names():**
  - Fetches available driver names from the database.

- **get_caregiver_options():**
  - Retrieves caregiver options for drivers.

- **get_car_options():**
  - Retrieves car options from the database.

- **get_data_from_database(table_name):**
  - Retrieves data from a specific table in the database.

- **get_drivers_from_database():**
  - Retrieves a list of drivers from the database.

- **get_courses_from_database():**
  - Retrieves a list of courses from the database.

- **fetch_results_from_database():**
  - Fetches race results from the database, including driver names, car models, ages, and course times.

- **determine_winner(results):**
  - Determines the winner based on race results.

- **get_sorted_results(results):**
  - Returns a sorted list of drivers based on their total race times.

- **get_top_4_drivers(results, winner):**
  - Retrieves the top 4 drivers based on their total race times, excluding the winner.

### Templates
- **adddriver.html:**
  - Template for adding a new driver.
  - Includes dynamic form elements based on user input.

- **admin.html:**
  - Main layout for the admin panel.
  - Contains navigation links to different sections.

- **base.html:**
  - Base layout template for other pages.
  - Includes a navigation bar with links to various sections.

- **courselist.html:**
  - Displays a list of courses.
  - Includes course information and images.

- **driver_details.html:**
  - Displays details of a specific driver and their runs.
  - Contains a form to select a driver and displays their information.

- **driverlist.html:**
  - Displays a list of drivers.
  - Includes driver information and highlights junior drivers.

- **driversearch.html:**
  - Template for searching drivers by name.
  - Includes a form for searching drivers and displays search results.

- **editruns.html:**
  - Template for editing runs for a specific driver and course.
  - Includes dropdowns for selecting a driver and course and allows editing run details.

- **junior_driver.html:**
  - Displays a list of junior drivers and their information.

- **overall_result.html:**
  - Displays overall results for drivers.
  - Includes winner information and details for each driver.

- **runs_list.html:**
  - Displays a list of run records.

- **searchresult.html:**
  - Displays search results for a specific driver.

- **top5graph.html:**
  - Displays a horizontal bar graph of the top 5 drivers.

## Assumptions
1. **Age Limit for Junior Drivers:**
   - Junior drivers must be less than 18 years old.
   - There is a specific category or classification for drivers under 18 years of age.

2. **Overall Result Calculation:**
   - Overall standings of drivers are determined by their cumulative course completion times.

3. **Top 5 Drivers Graph:**
   - The graph visualizes the performance of drivers based on the number of runs they have completed.

## Design Decisions
- Initially, I attempted to create a state-of-the-art design where multiple functionalities were integrated into a single page/code/route. However, I encountered difficulties, such as database update issues and handling errors.
- To address these challenges, I opted to create different routes and separate HTML templates for each specific case. For example, I initially tried to combine the "overall_result" and "top5graph" functionalities on a single page. Due to the complexity, I decided to separate them, allowing for easier handling and management of the functionalities.

## Database Questions
1. **SQL Statement to Create the "car" Table:**
   ```sql
   CREATE TABLE IF NOT EXISTS car
   (
   car_num INT PRIMARY KEY NOT NULL,
   model VARCHAR(20) NOT NULL,
   drive_class VARCHAR(3) NOT NULL
   );
   ```
   This statement creates the "car" table with fields for car number, model, and drive class.

2. **Setting up Relationship Between "car" and "driver" Tables:**
   - The "car" field in the "driver" table references the "car_num" field in the "car" table, establishing a relationship between drivers and their cars.

   ```sql
   FOREIGN KEY (car) REFERENCES car(car_num)
   ON UPDATE CASCADE
   ON DELETE CASCADE
   ```

3. **Inserting Mini and GR Yaris Details into the "car" Table:**
   ```sql
   INSERT INTO car VALUES
   (11, 'Mini', 'FWD'),
   (17, 'GR Yaris', '4WD');
   ```
   Inserts car details for Mini and GR Yaris into the "car" table.

4. **Setting Default Value for

 "driver_class" Field:**
   - To set a default value of 'RWD' for the "driver_class" field in the "car" table, you can modify the table creation statement like this:
   ```sql
   CREATE TABLE IF NOT EXISTS car
   (
   car_num INT PRIMARY KEY NOT NULL,
   model VARCHAR(20) NOT NULL,
   drive_class VARCHAR(3) DEFAULT 'RWD' NOT NULL
   );
   ```

5. **Importance of Different Routes for Drivers and Club Admin:**
      It's important for drivers and the club admin to access different routes in the web app for several reasons:

   a. **Data Privacy**: Drivers may have access to their own performance data and course information, while the club admin needs access to all drivers' data. Allowing drivers to access admin routes could compromise the privacy of other drivers' data.

   b. **Functionality Control**: The club admin may have additional functionalities, such as adding new drivers, courses, or managing overall results. Allowing drivers to access admin routes could lead to unintended changes to the system's configuration and data.

   c. **Security**: Access to certain routes may involve critical operations, such as modifying the database schema or managing user accounts. Allowing unauthorized users (drivers) to access these routes could lead to security vulnerabilities and potential data corruption.

   Examples of Problems if All Facilities Were Available to Everyone:
   - Unauthorized drivers modifying or deleting their own or others' run data.
   - Drivers accidentally altering the database schema or configuration settings.
   - Club admin inadvertently exposing sensitive driver information to all drivers.

To maintain data integrity, privacy, and security, it's essential to restrict access to specific routes based on user roles and permissions.
