from initializer import get_database_connection
from model.book import Book, tuple_to_book


class BookHelper:

    @staticmethod
    def add_book(book: Book):
        book_as_dictionary = book.to_dictionary()
        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO books VALUES (:bookID, :title, :authors, :average_rating, "
                ":isbn, :isbn13, :language_code, :num_pages, :ratings_count, :text_reviews_count, "
                ":publication_date, :publisher, :available)",
                book_as_dictionary)
            conn.commit()

    @staticmethod
    def view_book(book_id) -> Book:
        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books WHERE bookID=:bookID", {'bookID': book_id})
            book = cursor.fetchone()
            return tuple_to_book(book)

    @staticmethod
    def update_book(book: Book):
        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE books SET title=:title, authors=:authors, average_rating=:average_rating, "
                           "isbn=:isbn, isbn13=:isbn13, language_code=:language_code, num_pages=:num_pages, "
                           "ratings_count=:ratings_count, text_reviews_count=:text_reviews_count, "
                           "publication_date=:publication_date, publisher=:publisher, available=:available "
                           "WHERE bookID=:bookID", book.to_dictionary())
            conn.commit()

    @staticmethod
    def search(query: str) -> list[Book]:
        query = query.lower()
        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books WHERE "
                           "lower(title) LIKE :query OR "
                           "lower(authors) LIKE :query OR "
                           "lower(publisher) LIKE :query OR "
                           "publication_date LIKE :query",
                           {'query': '%' + query + '%'})
            books = cursor.fetchall()
            return list(map(tuple_to_book, books))

    @staticmethod
    def delete_book(book_id):
        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE bookID=:bookID", {'bookID': book_id})
            conn.commit()


