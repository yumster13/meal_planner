import mysql.connector
import csv
from django.db import models
class Ages(models.TextChoices):
    DEFAULT = '18+',
    PF = 'Petit F', 
    PG = 'Petit G', 
    GF = 'Grand F', 
    GG = 'Grand G',

class Status(models.TextChoices):
    C = 'En Cours',
    F = 'Fini',

class Mesurements(models.TextChoices):
    KG = 'KG',
    L = 'L', 
    PIECE = 'PIECE', 
    TRANCHE = 'TRANCHE', 
    CONDIMENT = 'CONDIMENT', 

class Moment(models.TextChoices):
    MATIN = "MATIN",
    MIDI = "MIDI",
    GOUTER = "GOUTER",
    SOUPER = "SOUPER",
    CINQIEME = "5EME",

class TypeCamp(models.TextChoices):
    MENU = "Menu",
    CAMP = "Camp",
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
            cursor.execute("select id from database_ingredient where name = %s",(row[0],))
            id = cursor.fetchall()
            print(id)
            if id:
                if row[1] == 'TRUE' and row[2] == 'TRUE' and row[3] == 'TRUE' and row[4] == 'TRUE':
                    cursor.execute("SELECT id from database_season where name = %s", ("Annee",))
                    season_id = cursor.fetchall()
                    cursor.execute("Insert into database_ingredient_season(ingredient_id,season_id) values (%s,%s)",(id[0][0],season_id[0][0]))
                else:
                    if row[1] == 'TRUE':
                        cursor.execute("SELECT id from database_season where name = %s", ("Ete",))
                        season_id = cursor.fetchall()
                        cursor.execute("Insert into database_ingredient_season(ingredient_id,season_id) values (%s,%s)",(id[0][0],season_id[0][0]))
                        
                    if row[2] == 'TRUE':
                        cursor.execute("SELECT id from database_season where name = %s", ("Automne",))
                        season_id = cursor.fetchall()
                        cursor.execute("Insert into database_ingredient_season(ingredient_id,season_id) values (%s,%s)",(id[0][0],season_id[0][0]))
                        
                    if row[3] == 'TRUE':
                        cursor.execute("SELECT id from database_season where name = %s", ("Hiver",))
                        season_id = cursor.fetchall()
                        cursor.execute("Insert into database_ingredient_season(ingredient_id,season_id) values (%s,%s)",(id[0][0],season_id[0][0]))
                        
                    if row[4] == 'TRUE':
                        cursor.execute("SELECT id from database_season where name = %s", ("Printemps",))
                        season_id = cursor.fetchall()
                        cursor.execute("Insert into database_ingredient_season(ingredient_id,season_id) values (%s,%s)",(id[0][0],season_id[0][0]))
                    
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
    host = 'MenuPlanner.mysql.pythonanywhere-services.com'
    user = 'MenuPlanner'
    password = 'sE@Z_PYC3gNL.$x'
    database = 'MenuPlanner$MEALPLANNER'

    # CSV file path
    csv_file = 'ingredients_saisons.csv'

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
