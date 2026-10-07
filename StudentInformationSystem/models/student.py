class Student:

    def __init__(
        self,
        student_id,
        first_name,
        last_name,
        age,
        gender,
        course,
        year_level,
        email
    ):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.course = course
        self.year_level = year_level
        self.email = email

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "gender": self.gender,
            "course": self.course,
            "year_level": self.year_level,
            "email": self.email
        }