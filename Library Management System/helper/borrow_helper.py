from datetime import datetime

# Importing the BookHelper class from books_helper.py, and the required functions and classes from other modules
from helper.books_helper import BookHelper
from initializer import get_database_connection
from model.book import Book, tuple_to_book
from model.borrowed_book import tuple_to_borrowed_book


class BorrowsHelper:

    # Static method to borrow a book for a user
    @staticmethod
    def borrow_book(user_id, book: Book):
        # Get the current date
        borrow_date = datetime.now().strftime("%Y-%m-%d")
        # Get a connection to the database
        with get_database_connection() as conn:
            cursor = conn.cursor()
            # Remove any reservations for the book by the user
            cursor.execute(
                "DELETE FROM reserved_books WHERE bookID = :book_id AND userID = :user_id",
                {"user_id": user_id, "book_id": book.bookID})
            # Add a new entry to the borrowed_books table for the user and book
            cursor.execute(
                "INSERT INTO borrowed_books (userID, bookID, borrow_date, status) "
                "VALUES (:user_id, :book_id, :borrow_date, 'borrowed')",
                {"user_id": user_id, "book_id": book.bookID, "borrow_date": borrow_date})
            # Commit the changes to the database
            conn.commit()
            # Decrement the available count of the book, and update the book in the database
            book.available = book.available - 1
            BookHelper.update_book(book)

    # Static method to return a borrowed book
    @staticmethod
    def return_book(borrow_id):
        # Get the current date
        return_date = datetime.now().strftime("%Y-%m-%d")
        # Get a connection to the database
        with get_database_connection() as conn:
            cursor = conn.cursor()
            # Update the borrowed_books entry for the given borrow_id, setting the return date and status to "returned"
            cursor.execute(
                "UPDATE borrowed_books SET return_date = :return_date, status = 'returned' WHERE borrowID = :borrow_id",
                {"return_date": return_date, "borrow_id": borrow_id})
            # Commit the changes to the database
            conn.commit()
            # Get the book ID from the borrowed_books entry
            cursor.execute(
                "SELECT * FROM borrowed_books WHERE borrowID = :borrow_id",
                {"borrow_id": borrow_id})
            borrow_tuple = cursor.fetchone()
            book_id = borrow_tuple[2]
            # Get the book information from the books table
            cursor.execute(
                "SELECT * FROM books WHERE bookID = :book_id",
                {"book_id": book_id})
            book_tuple = cursor.fetchone()
            book = tuple_to_book(book_tuple)
            # Increment the available count of the book, and update the book in the database
            book.available = book.available + 1
            BookHelper.update_book(book)

    # Static method to get a list of borrowed books for a given user
    @staticmethod
    def get_borrowed_books_for_user(user_id):
        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM borrowed_books WHERE userID = :user_id AND status = 'borrowed'",
                {"user_id": user_id})
            borrows_tuples = cursor.fetchall()

            borrows = []
            for borrow_tuple in borrows_tuples:
                book_id = borrow_tuple[2]
                cursor.execute(
                    "SELECT * FROM books WHERE bookID = :book_id",
                    {"book_id": book_id})
                book_tuple = cursor.fetchone()
                book = tuple_to_book(book_tuple)
                borrowed_book = tuple_to_borrowed_book(book, borrow_tuple)
                borrows.append(borrowed_book)
        return borrows

    @staticmethod
    def get_books(status: str):
        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM borrowed_books WHERE status = :status",
                {"status": status}
            )
            borrows_tuples = cursor.fetchall()
            borrows = []
            for borrow_tuple in borrows_tuples:
                book_id = borrow_tuple[2]
                cursor.execute(
                    "SELECT * FROM books WHERE bookID = :book_id",
                    {"book_id": book_id})
                book_tuple = cursor.fetchone()
                book = tuple_to_book(book_tuple)
                borrowed_book = tuple_to_borrowed_book(book, borrow_tuple)
                borrows.append(borrowed_book)
            return borrows

    @staticmethod
    def get_books_within_period(start_date: str, end_date: str):
        with get_database_connection() as conn: cursor = conn.cursor()
        cursor.execute("SELECT * FROM borrowed_books WHERE borrow_date >= :start_date and borrow_date <= :end_date",
                       {"start_date": start_date, "end_date": end_date})
        borrows_tuples = cursor.fetchall()
        borrows = []
        for borrow_tuple in borrows_tuples:
            book_id = borrow_tuple[2]
            cursor.execute("SELECT * FROM books WHERE bookID = :book_id",{"book_id": book_id})
            book_tuple = cursor.fetchone()
            book = tuple_to_book(book_tuple)
            borrowed_book = tuple_to_borrowed_book(book, borrow_tuple)
            borrows.append(borrowed_book)
            return borrows
