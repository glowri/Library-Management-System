from initializer import get_database_connection
from model.book import Book, tuple_to_book


class ReservationsHelper:

    @staticmethod
    def reserve_book(user_id, book: Book):
        # This function takes a user ID and a Book object as parameters and adds a new reservation for the book to the database.
        with get_database_connection() as conn:  # Open a connection to the database
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO reserved_books (userID, bookID) "
                "VALUES (:user_id, :book_id)",
                {"user_id": user_id, "book_id": book.bookID})  # Insert a new reservation into the reserved_books table, with the user ID and book ID as values

            conn.commit()  # Commit the transaction to the database


    @staticmethod
    def get_reservations(user_id):
        # This function takes a user ID as a parameter and returns a list of Book objects representing the books reserved by that user.
        with get_database_connection() as conn:  # Open a connection to the database
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM reserved_books WHERE userID = :user_id",
                {"user_id": user_id})  # Select all rows from the reserved_books table where the user ID matches the given user ID
            reservations_tuples = cursor.fetchall()  # Fetch all of the rows as tuples

            reserve_books = []  # Create an empty list to store the Book objects representing the reserved books
            for reservation_tuple in reservations_tuples:  # Iterate over each reservation tuple
                book_id = reservation_tuple[2]  # Get the book ID from the reservation tuple
                cursor.execute(
                    "SELECT * FROM books WHERE bookID = :book_id",
                    {"book_id": book_id})  # Select the row from the books table with the matching book ID
                book_tuple = cursor.fetchone()  # Fetch the row as a tuple
                reserved_book = tuple_to_book(book_tuple)  # Convert the book tuple to a Book object using the tuple_to_book function from the model.book module
                reserve_books.append(reserved_book)  # Add the Book object to the list of reserved books

            return reserve_books  # Return the list of reserved Book objects
