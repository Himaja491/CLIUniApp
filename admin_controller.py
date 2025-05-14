# admin_controller.py
from database import Database

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"


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
        print("no students to remove.")
        return

    student_id = input("Enter the ID of the student to remove: ").strip()

    updated_students = [s for s in students if s.id != student_id]

    if len(updated_students) == len(students):
        print("Student ID not found.")
    else:
        db.save_students(updated_students)
        print(f"Student with ID {student_id} has been removed.")






from database import Database
from student import Student
from subject import Subject

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

def admin_menu():
    db = Database()

    while True:
        print(f"{CYAN}Admin System (c/g/p/r/s/x):{RESET} ", end="")
        choice = input().strip().lower()

        if choice == 'c':
            clear_students(db)
        elif choice == 'g':
            group_students(db)
        elif choice == 'p':
            partition_students(db)
        elif choice == 'r':
            remove_student(db)
        elif choice == 's':
            show_students(db)
        elif choice == 'x':
            break
        else:
            print("Invalid option. Please try again.")

def show_students(db):
    print(f"{YELLOW}Student List{RESET}")
    students = db.load_students()
    if not students:
        print("< Nothing to Display >")
        return
    for student in students:
        print(f"{student.name} :: {student.id} --> Email: {student.email}")

def group_students(db):
    students = db.load_students()
    if not students:
        print("< Nothing to Display >")
        return

    print(f"{YELLOW}Grade Grouping{RESET}")
    grade_map = {}
    for s in students:
        for sub in s.subjects:
            if sub.grade not in grade_map:
                grade_map[sub.grade] = []
            grade_map[sub.grade].append((s.name, s.id, sub.grade, sub.mark))

    for grade, entries in grade_map.items():
        print(f"{grade}  --> ", end="")
        print("[", end="")
        print(", ".join(f"{name} :: {sid} --> GRADE: {grade} - MARK: {mark:.2f}" for name, sid, grade, mark in entries), end="")
        print("]")

def partition_students(db):
    students = db.load_students()
    print(f"{YELLOW}PASS/FAIL Partition{RESET}")
    if not students:
        print("FAIL --> []")
        print("PASS --> []")
        return

    pass_list = []
    fail_list = []

    for s in students:
        avg = s.calculate_average()
        info = f"{s.name} :: {s.id} --> GRADE: {s.get_grade_string()} - MARK: {avg:.2f}"
        if avg >= 50:
            pass_list.append(info)
        else:
            fail_list.append(info)

    print("FAIL --> [", end="")
    print(", ".join(fail_list), end="")
    print("]")

    print("PASS --> [", end="")
    print(", ".join(pass_list), end="")
    print("]")

def remove_student(db):
    students = db.load_students()
    if not students:
        print("No students to remove.")
        return

    sid = input("Remove by ID: ").strip()
    updated = [s for s in students if s.id != sid]

    if len(updated) == len(students):
        print(f"{RED}Student {sid} does not exist")
    else:
        db.save_students(updated)
        print(f"{YELLOW}Removing Student {sid} Account")

def clear_students(db):
    print("Clearing students database")
    confirm = input("Are you sure you want to clear the database (Y)ES/(N)O: ").strip().lower()
    if confirm == 'y' or confirm == 'yes':
        db.clear_students()
        print("Students data cleared")
    else:
        print("Operation cancelled.")
