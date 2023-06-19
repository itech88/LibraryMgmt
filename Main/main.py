import db_connector
from models import Library


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

        elif choice == "quit":
            break
        else:
            print(f"Must be a valid option, {choice} is not")
        my_library.close()


checkout()
