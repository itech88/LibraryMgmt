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
        self.library, self.cursor = get_db_cursor

    def add_book(
        self, title, author
    ):  # replace the add_book function with a database query
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
        self.cursor.mycursor.execute(
            "SELECT title, author, copies, available FROM Books WHERE title = %s and author = %s",
            (title, author),
        )
        myresult = self.cursor.mycursor.fetchall()

        if myresult:
            print("Book found in the library:")
            # print column headers
            column_names = [i[0] for i in self.cursor.mycursor.description]
            print(column_names)
            for x in myresult:
                print(x)
        elif not myresult:
            return "Book not found in the library"
