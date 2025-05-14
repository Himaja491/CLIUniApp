# main.py
from student_controller import student_menu
from admin_controller import CYAN, admin_menu
from database import Database 
import re

def university_menu():
    db = Database()
    db.initialize_file()
    while True:
        try:
            print(f"{CYAN}\nUniversity System : (A)dmin, (S)tudent, or X:")
            choice = input("Enter your choice: ").strip().upper()
            
            if choice == 'A':
                admin_menu()
            elif choice == 'S':
                student_menu()
            elif choice == 'X':
                print("Thank you")
                break
            else:
                print("Invalid choice. Please try A, S, or X.")
                
        except KeyboardInterrupt:
            print("\n\nForce quit detected. Saving data...")
            # Add any cleanup here if needed
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            # Log the error if needed

if __name__ == "__main__":
 # Ensure data file exists
    university_menu()