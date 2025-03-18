import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="2002"
)

my_cursor = mydb.cursor()

DB_NAME = 'miniart_db'

# my_cursor.execute(f"CREATE DATABASE {DB_NAME}")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)