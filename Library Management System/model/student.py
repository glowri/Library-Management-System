from model.user import User


class Student(User):
    def __init__(self, user_id, username, password, class_, full_name, fine):
        super().__init__(user_id, username, "student", password, full_name, fine)
        self.class_ = class_

    def to_dictionary(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "user_type": self.user_type,
            "password": self.password,
            "class_": self.class_,
            "department": None,
            "full_name": self.full_name
        }


def tuple_to_student(user_tuple):
    return Student(user_tuple[0], user_tuple[1], user_tuple[2], user_tuple[6], user_tuple[3], user_tuple[7])
