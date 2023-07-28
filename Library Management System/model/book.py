# Define a class called Book.
class Book:

    # Define the __init__ method to initialize the object's attributes.
    def __init__(self, bookID, title, authors, average_rating, isbn, isbn13, language_code, num_pages, ratings_count,
                 text_reviews_count, publication_date, publisher, available):
        # Initialize each attribute with the corresponding argument.
        self.bookID = bookID
        self.title = title
        self.authors = authors
        self.average_rating = average_rating
        self.isbn = isbn
        self.isbn13 = isbn13
        self.language_code = language_code
        self.num_pages = num_pages
        self.ratings_count = ratings_count
        self.text_reviews_count = text_reviews_count
        self.publication_date = publication_date
        self.publisher = publisher
        self.available = available

    def to_dictionary(self):
        # Define a method called to_dictionary that returns a dictionary representation of the Book object.
        return {
            'bookID': self.bookID,
            'title': self.title,
            'authors': self.authors,
            'average_rating': self.average_rating,
            'isbn': self.isbn,
            'isbn13': self.isbn13,
            'language_code': self.language_code,
            'num_pages': self.num_pages,
            'ratings_count': self.ratings_count,
            'text_reviews_count': self.text_reviews_count,
            'publication_date': self.publication_date,
            'publisher': self.publisher,
            'available': self.available
        }


# Define a method called is_available that returns True if the Book object is available, False otherwise.
    def is_available(self):
        return self.available > 0

# Define a function called tuple_to_book that takes a tuple as an argument and returns a new Book object.
def tuple_to_book(some: tuple) -> Book:
    return Book(
        bookID=some[0],
        title=some[1],
        authors=some[2],
        average_rating=some[3],
        isbn=some[4],
        isbn13=some[5],
        language_code=some[6],
        num_pages=some[7],
        ratings_count=some[8],
        text_reviews_count=some[9],
        publication_date=some[10],
        publisher=some[11],
        available=some[12]
    )
