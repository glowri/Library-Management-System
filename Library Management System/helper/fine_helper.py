from initializer import get_database_connection


class FineHelper:

    @staticmethod
    def add_fine(user_id, fine):
        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET fine = fine + :fine WHERE userID = :user_id",
                {"user_id": user_id, "fine": fine})

            conn.commit()

    @staticmethod
    def pay_fine(user_id):
        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET fine = 0 WHERE userID = :user_id",
                {"user_id": user_id})

            conn.commit()

    @staticmethod
    def get_fine(user_id):
        with get_database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE userID = :user_id",
                {"user_id": user_id})
            user_tuple = cursor.fetchone()
            return user_tuple[6]
