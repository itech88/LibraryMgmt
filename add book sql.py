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
    
    def add_book(self, title, author):
            title = title.lower()
            author = author.lower()
            new_book = (title, author)
            count = 0
            
            if (title, author) in self.books:
                count += 1
            else:
                self.books[(title, author)] = {'book': new_book, 'count': 1}
            return True
    
def checkout():
    book = Book('','') #empty strings a placeholder
    while True:
        choice = input('Pick a menu option: Add, Checkout, Return, Search, Quit: ').lower()
        if choice in ['add', 'checkout', 'return', 'search']:
            title = input('What is the book title? ')
            author = input('Who is the author? ')
            if choice == 'add':
                book.add_book(title, author)


