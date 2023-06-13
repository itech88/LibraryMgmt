import mysql.connector

# Create a connection to your MySQL database

library = mysql.connector.connect(
    host="localhost",
    user="root",
    password=input("password: "),
    database="library",  # directly select the database
)


mycursor = library.cursor()  # Create a cursor object to execute SQL commands


class Book:
    def __init__(self, title, author):
        self.title = title.lower()
        self.author = author.lower()
        self.status = "available"

    def __str__(self):
        return f"{self.title} by {self.author}, Status: {self.status}"

    def return_book(self, title, author):  # return a book to the library
        title = title.lower()
        author = author.lower()
        mycursor.execute(
            "SELECT title, author, copies, checked_out FROM Books WHERE title = %s and author = %s",
            (title, author),
        )
        myresult = mycursor.fetchall()

        if myresult:  # if the book exists in the library
            copies = myresult[0][2]
            checked_out = myresult[0][3]
            if checked_out > 0:  # if the book is checked out
                mycursor.execute(
                    "UPDATE Books SET checked_out = checked_out - 1 WHERE title = %s and author = %s",
                    (title, author),
                )
                library.commit()
                print(mycursor.rowcount, "record updated with a copy returned.")
                # Fetch the updated data
                mycursor.execute(
                    "SELECT title, author, copies, checked_out FROM Books WHERE title = %s and author = %s",
                    (title, author),
                )
                myresult = mycursor.fetchall()
                for x in myresult:
                    print(x)
                return True
            else:  # if the book is not checked out
                print("Sorry, there are no copies of that book checked out.")
                return False
        else:  # if the book does not exist in the library
            print("Sorry, that book is not in our library.")
            return False


def checkout():
    book = Book("", "")  # empty strings a placeholder
    while True:
        choice = input(
            "Pick a menu option: Add, Checkout, Return, Search, Quit: "
        ).lower()
        if choice in ["add", "checkout", "return", "search"]:
            title = input("What is the book title? ")
            author = input("Who is the author? ")
            if choice == "return":
                book.return_book(title, author)
        elif choice == "quit":
            break


checkout()

try:
    library = mysql.connector.connect(
        host="localhost",
        user="root",
        password=input("password: "),
        database="library",  # directly select the database
    )

    # Your database operations go here...

except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))

finally:
    if library.is_connected():
        library.close()
        print("MySQL connection is closed")
