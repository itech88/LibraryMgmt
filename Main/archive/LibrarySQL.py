import mysql.connector

# Create a connection to your MySQL database
library = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="library",  # directly select the database
)

# Create a cursor object to execute SQL commands
mycursor = library.cursor()


class Book:
    def __init__(self, title, author):
        self.title = title.lower()
        self.author = author.lower()
        self.status = "available"

    def __str__(self):
        return f"{self.title} by {self.author}, Status: {self.status}"


class Library:
    def __init__(self):
        self.books = {}
        self.catalog = mycursor.execute(
            "SELECT title, author FROM Books"
        )  # select all books from the database
        self.checked_out = {}

    def add_book(self, title, author):
        title = title.lower()
        author = author.lower()
        new_book = Book(title, author)

        if (title, author) in self.books:
            self.books[(title, author)]["count"] += 1
        else:
            self.books[(title, author)] = {"book": new_book, "count": 1}
        return True

    def checkout_book(self, title, author):
        title = title.lower()
        author = author.lower()
        self.catalog = mycursor.execute(
            "SELECT title, author FROM Books"
        )  # select all books from the database
        if (
            (title, author) in self.books
            and self.books[(title, author)]["count"] > 0
            and self.books[(title, author)]["book"].status == "available"
        ):
            self.books[(title, author)]["count"] -= 1
            if self.books[(title, author)]["count"] == 0:
                self.books[(title, author)]["book"].status = "checked out"
            self.checked_out[(title, author)] = (
                self.checked_out.get((title, author), 0) + 1
            )
            return True
        else:
            return False

    def return_book(self, title, author):
        title = title.lower()
        author = author.lower()
        if (title, author) in self.checked_out and self.checked_out[
            (title, author)
        ] > 0:
            self.checked_out[(title, author)] -= 1
            if self.checked_out[(title, author)] == 0:
                del self.checked_out[(title, author)]
            self.books[(title, author)]["count"] += 1
            self.books[(title, author)]["book"].status = "available"
            return True, self.books[(title, author)]["book"].status
        elif (title, author) in self.books:
            return False, "book was not checked out"
        else:
            return False, "not in library"

    def search(self, title, author):
        title = title.lower()
        author = author.lower()
        mycursor.execute(
            "SELECT title, author FROM Books WHERE title = %s and author = %s",
            (title, author),
        )
        myresult = mycursor.fetchall()
        if myresult:
            for x in myresult:
                print(x)
        else:
            return "Book not found in the library"
        # if (title, author) in self.books:
        #     book_info = self.books[(title, author)]
        #     return f"Title: {book_info['book'].title}, Author: {book_info['book'].author}, Status: {book_info['book'].status}, Copies: {book_info['count']}"
        # else:
        #     return "Book not found in the library"


def checkout():
    my_library = Library()

    while True:
        choice = input(
            "Pick a menu option: Add, Checkout, Return, Search, Quit: "
        ).lower()

        if choice in ["add", "checkout", "return", "search"]:
            title = input("What is the book title? ")
            author = input("Who is the author? ")

            if choice == "add":
                my_library.add_book(title, author)
                print(f"{title} by {author} added to library")

            elif choice == "checkout":
                if my_library.checkout_book(title, author):
                    print(f"Checkout of {title} by {author} was successful")
                else:
                    print(
                        f"Checkout unsuccessful, book not available or not in library"
                    )

            elif choice == "return":
                success, status = my_library.return_book(title, author)
                if success:
                    print(f"Return of {title} by {author} was successful")
                else:
                    print(f"Return unsuccessful, book {status}")

            elif choice == "search":
                print(my_library.search(title, author))
                # insert mysql search function here
            elif choice == "quit":
                break
            else:
                print(f"Must be a valid option, {choice} is not")


checkout()
