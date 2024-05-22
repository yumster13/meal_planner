import mysql.connector
import csv

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
            cursor.execute("Select id from database_recipe where name = %s",(row[0],))
            id = cursor.fetchall()
            if id is None:
                print(row[2])
                print(id)
                print((row[0],row[1],id[0][0],))
                cursor.execute("INSERT INTO database_recipe (name, prairie, tags_id) VALUES (%s, %s, %s)", (row[0],row[1],id[0][0],))
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
    csv_file = 'plats.csv'

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
