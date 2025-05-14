# student.py
import random

class Student:
    def __init__(self, name, email, password, subjects=None):
        self.id = str(random.randint(1, 999999)).zfill(6)  # 6-digit ID
        self.name = name
        self.email = email
        self.password = password
        self.subjects = subjects if subjects is not None else []

    def calculate_average(self):
        if not self.subjects:
            return 0
        return sum(subject.mark for subject in self.subjects) / len(self.subjects)

    def is_passed(self):
        return self.calculate_average() >= 50
    
    def get_grade_string(self):
        return ", ".join(subject.grade for subject in self.subjects)


    def __str__(self):
        subject_info = "\n".join(str(subj) for subj in self.subjects)
        return f"ID: {self.id}, Name: {self.name}, Email: {self.email}, Subjects:\n{subject_info if subject_info else 'None'}"
