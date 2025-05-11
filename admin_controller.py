# admin_controller.py
from database import Database

def admin_menu():
    db = Database()

    while True:
        print("\nAdmin System: (c)lear database, (g)roup students, (p)artition students, (r)emove student, (s)how students, (x)exit")
        choice = input("Enter your choice: ").strip().lower()

        if choice == 'c':
            confirm = input("Are you sure you want to clear the database? (yes/no): ").strip().lower()
            if confirm == 'yes':
                db.clear_students()
                print("All student data has been cleared.")
            else:
                print("Operation cancelled.")

        elif choice == 'g':
            group_students()

        elif choice == 'p':
            partition_students()

        elif choice == 'r':
            remove_student()

        elif choice == 's':
            show_students()

        elif choice == 'x':
            print("Returning to University Menu.")
            break

        else:
            print("Invalid choice. Please try again.")

def show_students():
    db = Database()
    students = db.load_students()

    if not students:
        print("No students found.")
        return

    print("\nList of Students:")
    for student in students:
        print(f"ID: {student.id}, Name: {student.name}, Email: {student.email}, Average Mark: {student.calculate_average():.2f}")

def group_students():
    db = Database()
    students = db.load_students()

    if not students:
        print("No students to group.")
        return

    groups = {}
    for student in students:
        for subject in student.subjects:
            if subject.grade not in groups:
                groups[subject.grade] = []
            groups[subject.grade].append((student.name, subject.id))

    print("\nGrouped Students by Grade:")
    for grade, info in groups.items():
        print(f"Grade {grade}:")
        for name, subject_id in info:
            print(f"  Student: {name}, Subject ID: {subject_id}")

def partition_students():
    db = Database()
    students = db.load_students()

    if not students:
        print("No students to partition.")
        return

    pass_list = [s for s in students if s.is_passed()]
    fail_list = [s for s in students if not s.is_passed()]

    print("\nPASS Students:")
    for student in pass_list:
        print(f"ID: {student.id}, Name: {student.name}, Avg: {student.calculate_average():.2f}")

    print("\nFAIL Students:")
    for student in fail_list:
        print(f"ID: {student.id}, Name: {student.name}, Avg: {student.calculate_average():.2f}")

def remove_student():
    db = Database()
    students = db.load_students()

    if not students:
        print("two students to remove.")
        return

    student_id = input("Enter the ID of the student to remove: ").strip()

    updated_students = [s for s in students if s.id != student_id]

    if len(updated_students) == len(students):
        print("Student ID not found.")
    else:
        db.save_students(updated_students)
        print(f"Student with ID {student_id} has been removed.")
