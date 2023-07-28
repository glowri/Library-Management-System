from model.user import User


# Define a class called Staff, which inherits from the User class.
class Staff(User):

    # Define the __init__ method to initialize the object's attributes.
    def __init__(self, user_id, username, password, department, full_name, fine):
        # Call the constructor of the parent class (User) using super(),
        # and pass it the required arguments. Also, pass "staff" as the user_type.
        super().__init__(user_id, username, "staff", password, full_name, fine)

        # Initialize the department attribute with the department argument.
        self.department = department

    # Define a method to convert the object's attributes into a dictionary.
    def to_dictionary(self):
        # Return a dictionary with the object's attributes as key-value pairs.
        # Note that the user_type is hardcoded as "staff", and class_ is set to None.
        return {
            "user_id": self.user_id,
            "username": self.username,
            "user_type": self.user_type,
            "password": self.password,
            "department": self.department,
            "class_": None,
            "full_name": self.full_name
        }


# Define a function called tuple_to_staff that takes a tuple as an argument.
def tuple_to_staff(user_tuple):
    # Create a new Staff object using the values in the tuple.
    # The values in the tuple are passed as arguments to the Staff constructor.
    # The order of the arguments is based on the order of the values in the tuple.
    # Note that the department value is in the 5th index of the tuple, and the full_name value is in the 3rd index.
    # Finally, return the new Staff object.
    return Staff(user_tuple[0], user_tuple[1], user_tuple[2], user_tuple[5], user_tuple[3], user_tuple[7])
