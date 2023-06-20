from db_connector import get_db_cursor


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
        self.checked_out = {}
        (
            self.library_db,
            self.cursor,
        ) = get_db_cursor()  # note the added parentheses here

    def add_book(self, title, author):
        title = title.lower()
        author = author.lower()

        self.cursor.execute(
            "SELECT title, author, copies, available FROM Books WHERE title = %s and author = %s",
            (title, author),
        )
        myresult = self.cursor.fetchall()

        if myresult:
            # if book already has a copy in the library, add one to the copies column
            self.cursor.execute(
                "UPDATE Books SET copies = copies + 1 WHERE title = %s and author = %s",
                (title, author),
            )
            self.library_db.commit()  # Use self.library_db to call the commit() method
            print(self.cursor.rowcount, "record updated with another copy.")
            for x in myresult:
                print(x)
            return True
        else:
            # Insert without explicitly setting the 'available' column
            self.cursor.execute(
                "INSERT INTO Books (title, author, copies) VALUES (%s, %s, 1)",
                (title, author),
            )
            self.library_db.commit()  # Use self.library_db to call the commit() method
            print(self.cursor.rowcount, "record inserted.")
            return True

    def checkout_book(self, title, author):
        title = title.lower()
        author = author.lower()
        self.cursor.execute(
            "SELECT title, author, copies, checked_out FROM Books WHERE title = %s and author = %s",
            (title, author),
        )
        myresult = self.cursor.fetchall()

        if myresult:  # if the book exists in the library
            copies = myresult[0][2]
            checked_out = myresult[0][3]
            if copies > checked_out:  # if the book is available
                self.cursor.execute(
                    "UPDATE Books SET checked_out = checked_out + 1 WHERE title = %s and author = %s",
                    (title, author),
                )
                self.library_db.commit()
                print(
                    self.cursor.rowcount,
                    "record(s) updated: a copy of the book has been checked out.",
                )
                # Fetch the updated data
                self.cursor.execute(
                    "SELECT title, author, copies, checked_out FROM Books WHERE title = %s and author = %s",
                    (title, author),
                )
                myresult = self.cursor.fetchall()
                for x in myresult:
                    print(x)
                return True
            else:  # if the book is not available
                print("Sorry, there are no copies of that book available.")
                return False
        else:  # if the book does not exist in the library
            print("Sorry, that book is not in our library.")
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
        self.cursor.execute(
            "SELECT title, author, copies, available FROM Books WHERE title = %s and author = %s",
            (title, author),
        )
        myresult = self.cursor.fetchall()

        if myresult:
            print("Book found in the library:")
            # print column headers
            column_names = [i[0] for i in self.cursor.description]
            print(column_names)
            for x in myresult:
                print(x)
        elif not myresult:
            return "Book not found in the library"
