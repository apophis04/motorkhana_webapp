import mysql.connector

dbuser = 'root'
dbpass = 'root'
dbhost = 'localhost'  # or the hostname where your MySQL server is running
dbname = 'motorkhana'

def create_db_connection():
    try:
        connection = mysql.connector.connect(
            user=dbuser,
            password=dbpass,
            host=dbhost,
            database=dbname,
            autocommit=True
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def close_db_connection(connection):
    if connection:
        connection.close()

if __name__ == "__main__":
    # This code is for testing the database connection
    connection = create_db_connection()
    if connection:
        print("Connected to the database successfully.")
        close_db_connection(connection)
