class User:
    def __init__(self, user_id, username, user_type, password, full_name, fine):
        self.user_id = user_id
        self.username = username
        self.user_type = user_type
        self.password = password
        self.full_name = full_name
        self.fine = fine

    def to_dictionary(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "user_type": self.user_type,
            "password": self.password,
            "full_name": self.full_name

        }
