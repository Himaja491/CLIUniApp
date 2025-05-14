# student_controller.py
import re
from admin_controller import CYAN, GREEN
from database import Database
from student import Student
from subject import Subject
def student_menu():
    while True:
        print(f"{CYAN}\nStudent System: (l/r/x): ")

        choice = input("Enter your choice: ").strip().lower()

        if choice == 'l':
            login_student()
        elif choice == 'r':
            register_student()
        elif choice == 'x':
            print("Returning to the University Menu.")
            break
        else:
            print("Invalid choice. Please try again.")

def register_student():
    print("\nStudent Registration Sign Up")
    name = input("Enter your full name: ").strip()
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").strip()

    # Validate email
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[uU]niversity\.com$", email):
        print("Invalid email format. Must end with @university.com")
        return

    # Validate password
    if not re.match(r"^[A-Z][a-zA-Z]{4,}\d{3,}$", password):
        print("Invalid password format. Must start with uppercase, 5+ letters, then 3+ digits.")
        return

    db = Database()
    students = db.load_students()

    # Check if email already exists
    if any(s.email.lower() == email.lower() for s in students):
        print("A student with this email already exists.")
        return

    # Create new student
    student = Student(name=name, email=email, password=password)
    students.append(student)
    db.save_students(students)
    print("Registration successful!")

def login_student():
    print(f"{GREEN}\nStudent Sign In")
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").strip()

    db = Database()
    students = db.load_students()

    # Find student
    student = next((s for s in students if s.email.lower() == email.lower() and s.password == password), None)
    if student:
        print(f"Welcome {student.name}!")
        subject_enrolment_menu(student, students, db)
    else:
        print("Invalid credentials. Please try again.")

def subject_enrolment_menu(student, all_students, db):
    while True:
        print("\nSubject Enrolment System: (c)hange password, (e)nrol, (r)emove subject, (s)how enrolment, (x)exit")
        choice = input("Enter your choice: ").strip().lower()

        if choice == 'c':
            new_password = input("Enter your new password: ").strip()
            if re.match(r"^[A-Z][a-zA-Z]{4,}\d{3,}$", new_password):
                student.password = new_password
                db.save_students(all_students)
                print("Password changed successfully.")
            else:
                print("Invalid password format.")
        
        elif choice == 'e':
            if len(student.subjects) >= 4:
                print("You cannot enrol in more than 4 subjects.")
            else:
                subject = Subject()
                student.subjects.append(subject)
                db.save_students(all_students)
                print(f"Subject enrolled successfully! Subject ID: {subject.id}, Mark: {subject.mark}, Grade: {subject.grade}")
        
        elif choice == 'r':
            if not student.subjects:
                print("No subjects to remove.")
            else:
                print("Your Subjects:")
                for subj in student.subjects:
                    print(f"{subj.id}: {subj.grade} ({subj.mark})")
                sub_id = input("Enter Subject ID to remove: ").strip()
                student.subjects = [s for s in student.subjects if str(s.id) != sub_id]
                db.save_students(all_students)
                print("Subject removed successfully.")
        
        elif choice == 's':
            if not student.subjects:
                print("No enrolled subjects.")
            else:
                print("Your Enrolled Subjects:")
                for subj in student.subjects:
                    print(f"ID: {subj.id}, Mark: {subj.mark}, Grade: {subj.grade}")
        
        elif choice == 'x':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")
