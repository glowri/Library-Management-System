from datetime import datetime
from typing import Callable

from helper.books_helper import BookHelper
from helper.borrow_helper import BorrowsHelper
from helper.fine_helper import FineHelper
from helper.reservations_helper import ReservationsHelper
from helper.user_helper import UserHelper, AuthenticationError
from misc.misc_functions import custom_input, just_list, input_with_type_validator
from model.book import Book
from model.borrowed_book import BorrowedBook
from model.librarian import Librarian
from model.staff import Staff
from model.student import Student
from model.user import User

# Define a search function that takes a function as input
# This function is used to search for books based on a quer
def search(function: Callable[[str], list[Book]]):
    print()
    print("Search")
    # Prompt the user to enter a search query
    query = input("Enter your search query: ")
    # Call the search function passed as input with the query
    books = function(query)

    # Create a list of book titles to display as options
    books_options = []
    for book in books:
        books_options.append(book.title)

    # Add a "Cancel" option to the end of the list
    books_options.append("Cancel")
    # Prompt the user to select a book from the list of options
    book_option_index = custom_input("Select a book (the number): ", books_options) - 1

    # If the user selects "Cancel", return None
    if book_option_index == len(books):
        return None

    # Otherwise, return the book selected by the user
    book = books[book_option_index]
    return book


# Define a user menu function that takes a user object as input
def user_menu(user: User):
    print()
    print(f"Welcome, {user.full_name}")
    # Prompt the user to select an option from a list of options
    user_option = custom_input("Enter your option: ",
                               ["Borrow Book", "Return Book", "Reserve Book", "View Reserved Books", "Pay Fine",
                                "Logout"])

    # Define a function for listing borrowed books
    def list_borrowed_books(books: list[BorrowedBook]):
        print()
        print("Select book")
        # Create a list of book titles and the date they were borrowed to display as options
        books_options = []
        for book in books:
            books_options.append(f"{book.title}\nBorrowed on: {book.borrow_date}")
            # Add a "Cancel" option to the end of the list
        books_options.append("Cancel")
        # Prompt the user to select a book from the list of options
        book_option_index = custom_input("Select a book (the number): ", books_options) - 1

        # If the user selects "Cancel", return None
        if book_option_index == len(books):
            return None

        # Otherwise, return the book selected by the user
        book = books[book_option_index]
        return book

    # Function to display a list of reserved books for the user
    def list_reserved_books(books: list[Book]):
        print()
        print("Reserved books")
        books_options = []
        # Iterate through each book in the list and add its title and availability status to a list of book options
        for book in books:
            books_options.append(f"{book.title}\nAvailable: {book.is_available()}")

        # Call the helper function just_list to display the list of book options to the user
        just_list(books_options)

    # Function to allow the user to borrow a book
    def borrow_book():
        # Check if the user has a fine, and if so, display a message and prevent borrowing until the fine is paid
        if user.fine > 0:
            print("You have a fine of ", user.fine, "\nPlease pay it before borrowing a book")
        else:
            # Get a list of books currently borrowed by the user
            borrows = BorrowsHelper.get_borrowed_books_for_user(user.user_id)
            # If the user has already borrowed the maximum number of books, display a message and prevent borrowing
            if len(borrows) == 5:
                print("You have reached the maximum number of borrowed books")
            else:
                # Allow the user to search for a book by title or author, and return the selected book
                selected_book = search(BookHelper.search)
                if selected_book is not None:
                    if not selected_book.is_available():
                        print("This book is not available")
                    else:
                        # If the selected book is not available, display a message and prevent borrowing
                        selected_book_id = selected_book.bookID
                        borrows_ids = []
                        for borrow in borrows:
                            borrows_ids.append(borrow.bookID)
                            # If the selected book is available, check if the user has already borrowed it
                        if selected_book_id in borrows_ids:
                            print("You have already borrowed this book")
                        else:
                            # If the book is available and the user has not already borrowed it, allow the user to borrow it
                            BorrowsHelper.borrow_book(user.user_id, selected_book)
                            print("Book borrowed successfully \nPlease return the book on/before the due date"
                                  " Failure to do this attracts GBP2 per day")
        # After the user borrows or attempts to borrow a book, return to the user menu
        user_menu(user)

    # Function to allow the user to return a borrowed book
    def return_book():
        # Get a list of books currently borrowed by the user
        borrows = BorrowsHelper.get_borrowed_books_for_user(user.user_id)
        # If the user has no borrowed books, display a message and prevent returning a book
        if len(borrows) == 0:
            print("You have no borrowed books")
        else:
            # Allow the user to select a borrowed book from the list of borrowed books, and return the selected book
            selected_borrowed_book = list_borrowed_books(borrows)
            if selected_borrowed_book is not None:
                # Calculate the number of days the book was borrowed, and if it is more than 7 days, add a fine to the user's account

                current_date = datetime.now()
                borrow_date = datetime.strptime(selected_borrowed_book.borrow_date, "%Y-%m-%d")
                defaulting_days = (current_date - borrow_date).days
                debt = defaulting_days * 2

                if defaulting_days > 7:
                    FineHelper.add_fine(user.user_id, debt)
                    print(f"You have a fine of GBP{debt} for returning the book late")
                else:
                    BorrowsHelper.return_book(selected_borrowed_book.borrowID)
                    print("Book returned successfully")
        user_menu(user)

    def reserve_book():
        # Search for a book to reserve
        selected_book = search(BookHelper.search)
        if selected_book is not None:
            # Reserve the selected book
            ReservationsHelper.reserve_book(user.user_id, selected_book)
            print("Book reserved successfully")
        user_menu(user)

    def view_reserved_books():
        # Get a list of reserved books for the user
        reserved_books = ReservationsHelper.get_reservations(user.user_id)
        if len(reserved_books) == 0:
            # If no reserved books, inform user
            print("You have no reserved books")
        else:
            # Print a list of reserved books with their availability
            list_reserved_books(reserved_books)
        user_menu(user)

    def pay_fine():
        if user.fine == 0:
            # If no fine, inform user
            print("You have no fine")

        else:
            # If there is a fine, ask user if they want to pay it
            print(f"You have a fine of {user.fine}")
            pay_fine_option = custom_input("Select an option: ", ["YES", "NO"])
            if pay_fine_option == 1:
                # If user chooses to pay fine, update fine to 0 and inform user
                FineHelper.pay_fine(user.user_id)
                user.fine = 0
                print("Fine paid successfully")
            else:
                # If user chooses not to pay fine, inform user
                print("Fine not paid")
        user_menu(user)

    if user_option == 1:
        # Borrow book
        borrow_book()
    elif user_option == 2:
        #return book
        return_book()
    elif user_option == 3:
        reserve_book()
    elif user_option == 4:
        view_reserved_books()
    elif user_option == 5:
        pay_fine()


def librarian_menu(librarian: Librarian):
    print()
    print(f"Welcome, {librarian.full_name}")
    # Present options to the librarian
    user_option = custom_input("Enter your option: ",
                               ["Add Book", "Update Book", "Delete Book", "View Reports",
                                "Logout"])

    def add_book():
        print()
        print("Add book")
        book_id = int(datetime.now().strftime('%m%d%S'))
        title = input_with_type_validator("Enter book title: ")
        authors = input_with_type_validator("Enter book authors: ")
        average_rating = input_with_type_validator("Enter book average rating(number): ", float)
        isbn = input_with_type_validator("Enter book isbn(number): ", int)
        isbn13 = input_with_type_validator("Enter book isbn13(number): ", int)
        language_code = input_with_type_validator("Enter book language code: ")
        num_pages = input_with_type_validator("Enter book number of pages(number): ", int)
        ratings_count = input_with_type_validator("Enter book ratings count(number): ", int)
        text_reviews_count = input_with_type_validator("Enter book text reviews count(number): ", int)
        publication_date = input_with_type_validator("Enter book publication date: ")
        publisher = input_with_type_validator("Enter book publisher: ")
        available = input_with_type_validator("Enter book availability(number): ", int)

        book = Book(book_id, title, authors, average_rating, isbn, isbn13, language_code, num_pages, ratings_count,
                    text_reviews_count, publication_date, publisher, available)
        BookHelper.add_book(book)
        print("Book added successfully")
        librarian_menu(librarian)

    def update_book():
        print()
        print("Update book")
        selected_book = search(BookHelper.search)
        if selected_book is not None:
            print()
            book_id = selected_book.bookID
            title = input_with_type_validator("Enter book title: ")
            authors = input_with_type_validator("Enter book authors: ")
            average_rating = input_with_type_validator("Enter book average rating(number): ", float)
            isbn = input_with_type_validator("Enter book isbn(number): ", int)
            isbn13 = input_with_type_validator("Enter book isbn13(number): ", int)
            language_code = input_with_type_validator("Enter book language code: ")
            num_pages = input_with_type_validator("Enter book number of pages(number): ", int)
            ratings_count = input_with_type_validator("Enter book ratings count(number): ", int)
            text_reviews_count = input_with_type_validator("Enter book text reviews count(number): ", int)
            publication_date = input_with_type_validator("Enter book publication date: ")
            publisher = input_with_type_validator("Enter book publisher: ")
            available = input_with_type_validator("Enter book availability(number): ", int)

            book = Book(book_id, title, authors, average_rating, isbn, isbn13, language_code, num_pages, ratings_count,
                        text_reviews_count, publication_date, publisher, available)
            BookHelper.update_book(book)
            print("Book updated successfully")
        librarian_menu(librarian)

    def delete_book():
        print()
        print("Delete book")
        selected_book = search(BookHelper.search)
        if selected_book is not None:
            yes_or_no = custom_input("Select an option: ", ["YES", "NO"])

            if yes_or_no == 1:
                BookHelper.delete_book(selected_book.bookID)
                print("Book deleted successfully")

        librarian_menu(librarian)

    def view_reports():
        def list_books(status: str, books: list[BorrowedBook]):
            print()
            print(f"{status.capitalize()} books")
            books_options = []
            for book in books:
                text = book.title
                text += f"\nBorrow date: {book.borrow_date}"
                if status == 'returned':
                    text += f"\nReturn date: {book.return_date}"
                books_options.append(f"{text}")

            just_list(books_options)

        print()
        print("Reports")
        options = custom_input("Select an option: ", ["View borrowed books", "View returned books",
                                                      "View books borrowed from:", "Cancel"])
        if options == 1:
            borrowed_books = BorrowsHelper.get_books('borrowed')
            if len(borrowed_books) == 0:
                print("No borrowed books")
            else:
                list_books('borrowed', borrowed_books)
        elif options == 2:
            returned_books = BorrowsHelper.get_books('returned')
            if len(returned_books) == 0:
                print("No returned books")
            else:
                list_books('returned', returned_books)
        elif options == 3:
            start_date = input_with_type_validator("Enter start date (yyyy-mm-dd): ")
            end_date = input_with_type_validator("Enter end date (yyyy-mm-dd): ")
            borrowed_books = BorrowsHelper.get_books_within_period(start_date, end_date)
            if len(borrowed_books) == 0:
                print("No borrowed books within this period")
            else:
                list_books('borrowed', borrowed_books)

        librarian_menu(librarian)

    if user_option == 1:
        add_book()
    elif user_option == 2:
        update_book()
    elif user_option == 3:
        delete_book()
    elif user_option == 4:
        view_reports()


def register():
    try:
        print()
        print("Register")
        user_type = custom_input("Enter your user type: ", ["Student", "Staff", "Librarian"])
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        full_name = input("Enter your full name: ")
        if user_type == 1:
            student_class = input("Enter your class: ")
            student = Student(None, username, password, student_class, full_name, 0)
            UserHelper.register_user(student)
            user_menu(student)
            return
        elif user_type == 2:
            department = input("Enter your department: ")
            staff = Staff(None, username, password, department, full_name, 0)
            UserHelper.register_user(staff)
            user_menu(staff)
            return

        librarian = Librarian(None, username, password, full_name)

        UserHelper.register_librarian(librarian)
        librarian_menu(librarian)
    except AuthenticationError as e:
        print(e.message)
        register()


def login():
    print()
    print(f"Login")
    user_type = custom_input("Enter your user type: ", ["Student", "Staff", "Librarian"])
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if user_type == 1 or user_type == 2:
        user = UserHelper.login_user(username, password)
    else:
        user = UserHelper.login_librarian(username, password)

    if user is None:
        print("Invalid username or password")
        login()
    elif user_type == 1 or user_type == 2:
        user_menu(user)
    else:
        librarian_menu(user)


print("Welcome to our Library System")
print("Please select an option from the menu below:")
option = custom_input("Enter your option: ", ["Register", "Login", "Exit"])
if option == 1:
    register()
elif option == 2:
    login()
elif option == 3:
    pass
