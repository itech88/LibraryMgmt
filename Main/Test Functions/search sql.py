import mysql.connector

# Create a connection to your MySQL database
library = mysql.connector.connect(
    host="localhost",
    user="root",
    password=input("password: "),
    database="library",  # directly select the database
)

# Create a cursor object to execute SQL commands
mycursor = library.cursor()


class Book:
    def __init__(self, title, author, status):
        self.title = title.lower()
        self.author = author.lower()
        self.status = status

    def __str__(self):
        return f"{self.title} by {self.author}, Status: {self.status}"

    def search(self, title, author):
        title = title.lower()
        author = author.lower()
        mycursor.execute(
            "SELECT title, author, copies, available FROM Books WHERE title = %s and author = %s",
            (title, author),
        )
        myresult = mycursor.fetchall()
        print(type(myresult))

        if myresult:
            print("Book found in the library:")
            # print column headers
            column_names = [i[0] for i in mycursor.description]
            print(column_names)
            for x in myresult:
                print(x)
        elif not myresult:
            print("Book not found in the library")  # change to return in real script


def checkout():
    while True:
        choice = input(
            "Pick a menu option: Add, Checkout, Return, Search, Quit: "
        ).lower()
        if choice in ["add", "checkout", "return", "search"]:
            title = input("What is the book title? ")
            author = input("Who is the author? ")
            if choice == "search":
                book = Book(title, author, "")
                book.search(title, author)


checkout()

# Close the cursor and connection at the end
mycursor.close()
library.close()
