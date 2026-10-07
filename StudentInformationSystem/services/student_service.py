import json
import os
from models.student import Student
from utils.logger import setup_logger


class StudentService:

    def __init__(self, data_file):

        self.data_file = data_file
        self.logger = setup_logger()

        self._create_data_file()

    def _create_data_file(self):

        folder = os.path.dirname(self.data_file)

        if not os.path.exists(folder):
            os.makedirs(folder)

        if not os.path.exists(self.data_file):

            with open(
                self.data_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    [],
                    file,
                    indent=4
                )

    def _load_students(self):

        try:

            with open(
                self.data_file,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except (json.JSONDecodeError, FileNotFoundError):

            self.logger.error(
                "Unable to read student data file."
            )

            return []

    def _save_students(self, students):

        try:

            with open(
                self.data_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    students,
                    file,
                    indent=4
                )

            return True

        except OSError as error:

            self.logger.error(
                f"Error saving students: {error}"
            )

            return False

    def get_all_students(self):

        return self._load_students()

    def get_student(self, student_id):

        students = self._load_students()

        for student in students:

            if student["student_id"] == student_id:
                return student

        return None

    def add_student(self, data):

        required_fields = [
            "student_id",
            "first_name",
            "last_name",
            "age",
            "gender",
            "course",
            "year_level",
            "email"
        ]

        for field in required_fields:

            if not data.get(field):

                return False, f"{field.replace('_', ' ').title()} is required."

        if self.get_student(data["student_id"]):

            return False, "Student ID already exists."

        try:

            age = int(data["age"])

            if age < 1 or age > 100:
                return False, "Age must be between 1 and 100."

            data["age"] = age

        except ValueError:

            return False, "Age must be a valid number."

        student = Student(**data)

        students = self._load_students()

        students.append(
            student.to_dict()
        )

        if self._save_students(students):

            self.logger.info(
                f"Student added: {data['student_id']}"
            )

            return True, "Student added successfully."

        return False, "Unable to save student record."

    def update_student(self, student_id, data):

        students = self._load_students()

        found = False

        try:

            age = int(data["age"])

            if age < 1 or age > 100:
                return False, "Age must be between 1 and 100."

            data["age"] = age

        except ValueError:

            return False, "Age must be a valid number."

        for index, student in enumerate(students):

            if student["student_id"] == student_id:

                data["student_id"] = student_id

                students[index] = data

                found = True

                break

        if not found:

            return False, "Student record was not found."

        if self._save_students(students):

            self.logger.info(
                f"Student updated: {student_id}"
            )

            return True, "Student information updated successfully."

        return False, "Unable to update student record."

    def delete_student(self, student_id):

        students = self._load_students()

        updated_students = [
            student
            for student in students
            if student["student_id"] != student_id
        ]

        if len(updated_students) == len(students):

            return False, "Student record was not found."

        if self._save_students(updated_students):

            self.logger.info(
                f"Student deleted: {student_id}"
            )

            return True, "Student deleted successfully."

        return False, "Unable to delete student record."

    def search_students(self, keyword):

        students = self._load_students()

        keyword = keyword.lower()

        results = []

        for student in students:

            searchable_data = [
                student["student_id"],
                student["first_name"],
                student["last_name"],
                student["course"],
                student["year_level"],
                student["email"]
            ]

            if any(
                keyword in str(value).lower()
                for value in searchable_data
            ):
                results.append(student)

        return results