import inspect
import json
import os
import sqlite3


def get_database_connection() -> sqlite3.Connection:
    script_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    __db_path = os.path.join(script_path, "mydb.db")
    return sqlite3.connect(__db_path)


conn = get_database_connection()
conn.execute("PRAGMA foreign_keys = ON;")
cursor = conn.cursor()


def create_book_table():
    cursor.execute('CREATE TABLE IF NOT EXISTS books (bookID INTEGER PRIMARY KEY, title TEXT, authors TEXT, '
                   'average_rating REAL, isbn INTEGER, isbn13 INTEGER, language_code TEXT, num_pages INTEGER, '
                   'ratings_count INTEGER, text_reviews_count INTEGER, publication_date TEXT, publisher TEXT, '
                   'available INTEGER)')
    conn.commit()

    with open('books.json', encoding='utf-8') as f:
        data = json.load(f)
        for book in data:
            cursor.execute("INSERT INTO books VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (
                book['bookID'], book['title'], book['authors'], book['average_rating'], book['isbn'], book['isbn13'],
                book['language_code'], book['num_pages'], book['ratings_count'], book['text_reviews_count'],
                book['publication_date'], book['publisher'], 4))
        conn.commit()


def create_user_table():
    cursor.execute('CREATE TABLE IF NOT EXISTS users '
                   '(userID INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, full_name TEXT, '
                   'user_type TEXT, department TEXT, class TEXT, fine REAL)')
    conn.commit()


def create_borrowed_books_table():
    cursor.execute('CREATE TABLE IF NOT EXISTS borrowed_books '
                   '(borrowID INTEGER PRIMARY KEY AUTOINCREMENT, userID INTEGER, bookID INTEGER, '
                   'borrow_date TEXT, return_date TEXT, status TEXT, '
                   'FOREIGN KEY(userID) REFERENCES users(userID), '
                   'FOREIGN KEY(bookID) REFERENCES books(bookID))')
    conn.commit()


def create_reserved_books_table():
    cursor.execute('CREATE TABLE IF NOT EXISTS reserved_books '
                   '(reservationID INTEGER PRIMARY KEY AUTOINCREMENT, userID INTEGER, bookID INTEGER, '
                   'FOREIGN KEY(userID) REFERENCES users(userID), '
                   'FOREIGN KEY(bookID) REFERENCES books(bookID))')
    conn.commit()


#create_book_table()
create_user_table()
create_borrowed_books_table()
create_reserved_books_table()
