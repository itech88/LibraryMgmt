import mysql.connector

def get_db_cursor():
    library = mysql.connector.connect(
      host="localhost",
      user="root",
      password=input("password: "),
      database="library"  # directly select the database
    )

    mycursor = library.cursor()

    return library, mycursor
