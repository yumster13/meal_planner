import mysql.connector
import csv
from .meal_planner.database.models import *

# Connect to MySQL
def connect_to_mysql(host, user, password, database):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4'
        )
        print("Connected to MySQL database with UTF-8 charset")
        return conn
    except mysql.connector.Error as err:
        print("Error connecting to MySQL:", err)
        return None

# Read data from CSV file
def read_csv(file_path):
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                data.append(row)
        print("CSV file read successfully")
        return data
    except FileNotFoundError:
        print("CSV file not found")
        return None
    except Exception as e:
        print("Error reading CSV file:", e)
        return None

# Insert data into MySQL table
def insert_into_mysql(conn, data):
    if conn is None or data is None:
        return

    cursor = conn.cursor()
    try:
        for row in data:
            print(row)
            cursor.execute("select name from database_engredient where name = %s",(row[0]))
            id = cursor.fetchall()
            for element in len(row)-1:
                cursor.execute("SELECT id from database_season where name = %s", (row[element-1]))
                category_id = cursor.fetchall()
                cursor.execute("Insert into database_category(ingredient_id,category_id) values (%s,%s)",(id[0][0],category_id[0][0]))
                
            conn.commit()
        print("Data inserted into MySQL table")
    except mysql.connector.Error as err:
        print("Error inserting data into MySQL:", err)
        conn.rollback()
    finally:
        cursor.close()

# Main function
def main():
    # MySQL connection details
    host = 'localhost'
    user = 'user'
    password = 'user_local'
    database = 'meal_planner'

    # CSV file path
    csv_file = 'recettes.csv'

    # Connect to MySQL
    conn = connect_to_mysql(host, user, password, database)
    if conn is None:
        return

    # Read data from CSV
    data = read_csv(csv_file)
    if data is None:
        return

    # Insert data into MySQL
    insert_into_mysql(conn, data)

    # Close MySQL connection
    conn.close()

if __name__ == "__main__":
    main()
