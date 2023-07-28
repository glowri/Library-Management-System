from initializer import get_database_connection
from model.librarian import Librarian, tuple_to_librarian
from model.staff import tuple_to_staff
from model.student import tuple_to_student
from model.user import User


class UserHelper:
    """
        A helper class for user-related operations.
        """

    @classmethod
    def is_user_name_available(cls, username):
        """
              Check if a username is available in the database.
              """
        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = :username",
                {"username": username})
            user_tuple = cursor.fetchone()
            return user_tuple is None

    @classmethod
    def register_user(cls, user: User):
        user_as_dictionary = user.to_dictionary()

        if not cls.is_user_name_available(user.username):
            raise AuthenticationError("Username is already taken")

        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users "
                "(username, user_type, password, department, class, fine, full_name) "
                "VALUES (:username, :user_type, :password, :department, :class_, 0, :full_name)",
                user_as_dictionary)
            conn.commit()
        return user

    @classmethod
    def register_librarian(cls, librarian: Librarian):
        librarian_as_dictionary = librarian.to_dictionary()

        if not cls.is_user_name_available(librarian.username):
            raise AuthenticationError("Username is already taken")

        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users "
                "(username, user_type, password, full_name) "
                "VALUES (:username, :user_type, :password, :full_name)",
                librarian_as_dictionary)
            conn.commit()
        return librarian

    @staticmethod
    def login_user(username, password):
        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = :username AND password = :password",
                {"username": username, "password": password})
            user_tuple = cursor.fetchone()
            if user_tuple is None:
                return None
            if user_tuple[3] == "student":
                return tuple_to_student(user_tuple)
            return tuple_to_staff(user_tuple)

    @staticmethod
    def login_librarian(username, password):
        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = :username AND password = :password",
                {"username": username, "password": password})
            user_tuple = cursor.fetchone()
            if user_tuple is None:
                return None
            return tuple_to_librarian(user_tuple)


class AuthenticationError(Exception):

    def __init__(self, message):
        self.message = message
