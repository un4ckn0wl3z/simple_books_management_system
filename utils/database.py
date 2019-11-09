from .database_connection import DatabaseConnection
from exceptions.duplicate_book_exception import DuplicateBookException

"""
Concern with storing and retrieving books from a json file.
"""
db = 'data.db'


def create_book_table():
    with DatabaseConnection(db) as connection:
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS books(name text primary key, author text, read integer)')


def add_book(name, author):
    with DatabaseConnection(db) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute('INSERT INTO books VALUES(?, ?, 0)', (name, author))
        except Exception:
            raise DuplicateBookException('This book has already in database.', 500)


def get_all_book():
    with DatabaseConnection(db) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM books')
        books = [{"name": row[0], "author": row[1], "read": row[2]} for row in cursor.fetchall()]
    return books


def mark_book_as_read(name):
    with DatabaseConnection(db) as connection:
        cursor = connection.cursor()
        cursor.execute('UPDATE books SET read=1 WHERE name=?', (name,))


def delete_book(name):
    with DatabaseConnection(db) as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM books WHERE name=?', (name,))
