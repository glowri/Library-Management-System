from model.book import Book


class BorrowedBook(Book):

    def __init__(self, book: Book, borrowID, status, borrow_date, return_date):
        super().__init__(
            bookID=book.bookID,
            title=book.title,
            authors=book.authors,
            average_rating=book.average_rating,
            isbn=book.isbn,
            isbn13=book.isbn13,
            language_code=book.language_code,
            num_pages=book.num_pages,
            ratings_count=book.ratings_count,
            text_reviews_count=book.text_reviews_count,
            publication_date=book.publication_date,
            publisher=book.publisher,
            available=book.available
        )
        self.status = status
        self.borrow_date = borrow_date
        self.return_date = return_date
        self.borrowID = borrowID


def tuple_to_borrowed_book(book: Book, borrow_tuple):
    return BorrowedBook(
        book=book,
        borrowID=borrow_tuple[0],
        borrow_date=borrow_tuple[3],
        return_date=borrow_tuple[4],
        status=borrow_tuple[5]
    )
