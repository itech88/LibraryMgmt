import mysql.connector

# Create a connection to your MySQL database
library = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="library"  # directly select the database
)

# Create a cursor object to execute SQL commands
mycursor = library.cursor()

class Book:
    def __init__(self, title, author):
        self.title = title.lower()
        self.author = author.lower()
        self.status = 'available'

    def __str__(self):
        return f"{self.title} by {self.author}, Status: {self.status}"


    def search(self, title, author):
            title = title.lower()
            author = author.lower()
            mycursor.execute("SELECT title, author FROM Books WHERE title = %s and author = %s", (title, author))
            myresult = mycursor.fetchall()
            if myresult:
                for x in myresult:
                    print(x)
            else:
                return "Book not found in the library"
    

def checkout():
    book = Book('','') #empty strings a placeholder
    while True:
        choice = input('Pick a menu option: Add, Checkout, Return, Search, Quit: ').lower()
        if choice in ['add', 'checkout', 'return', 'search']:
            title = input('What is the book title? ')
            author = input('Who is the author? ')
            if choice == 'search':
                book.search(title, author)
                
                

checkout()

