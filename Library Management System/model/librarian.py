class Librarian:
    # Define a class called Librarian
    def __init__(self, user_id, username, password, full_name):
        # Initialize the instance variables with the values passed as parameters
        self.user_id = user_id
        self.username = username
        self.user_type = "librarian"
        self.password = password
        self.full_name = full_name

    def to_dictionary(self):
        # Convert the instance variables to a dictionary and return it
        return {
            "user_id": self.user_id,
            "username": self.username,
            "user_type": self.user_type,
            "password": self.password,
            "full_name": self.full_name
        }


def tuple_to_librarian(user_tuple):
    # Convert a tuple of user information to a Librarian object and return it
    return Librarian(user_tuple[0], user_tuple[1], user_tuple[2], user_tuple[3])
