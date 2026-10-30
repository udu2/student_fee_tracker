import json
import os
import uuid
from datetime import datetime

DATA_FILE = "students.json"
RECEIPT_FOLDER = "receipts"


# Load student records
def load_students():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}


# Save student records
def save_students(students):
    with open(DATA_FILE, "w") as file:
        json.dump(students, file, indent=4)


# Register a student
def register_student(students):
    student_id = input("Enter student ID: ")

    if student_id in students:
        print("Student ID already exists.")
        return

    name = input("Enter student name: ")
    parent = input("Enter parent's name: ")
    email = input("Enter parent's email: ")
    fees = float(input("Enter total school fees: "))

    if fees <= 0:
        print("School fees must be greater than zero.")
        return

    students[student_id] = {
        "name": name,
        "parent": parent,
        "email": email,
        "fees": fees,
        "payments": []
    }

    save_students(students)
    print("Student registered successfully!")


# Record a payment
def record_payment(students):
    student_id = input("Enter student ID: ")

    if student_id not in students:
        print("Student not found.")
        return

    student = students[student_id]

    paid = sum(p["amount"] for p in student["payments"])
    balance = student["fees"] - paid

    print(f"Outstanding balance: ₦{balance:,.2f}")

    if balance <= 0:
        print("All fees have been paid.")
        return

    amount = float(input("Enter payment amount: "))

    if amount <= 0 or amount > balance:
        print("Invalid payment amount.")
        return

    receipt_number = str(uuid.uuid4())[:8].upper()

    payment = {
        "receipt": receipt_number,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    student["payments"].append(payment)
    save_students(students)

    generate_receipt(student, payment)

    print("Payment recorded successfully!")
    print(f"Receipt number: {receipt_number}")


# Generate a receipt
def generate_receipt(student, payment):
    os.makedirs(RECEIPT_FOLDER, exist_ok=True)

    total_paid = sum(
        p["amount"] for p in student["payments"]
    )

    balance = student["fees"] - total_paid

    filename = os.path.join(
        RECEIPT_FOLDER,
        f"{payment['receipt']}.txt"
    )

    with open(filename, "w") as file:
        file.write("SCHOOL FEE PAYMENT RECEIPT\n")
        file.write("=" * 35 + "\n")
        file.write(f"Student: {student['name']}\n")
        file.write(f"Parent: {student['parent']}\n")
        file.write(f"Receipt Number: {payment['receipt']}\n")
        file.write(f"Payment Date: {payment['date']}\n")
        file.write(f"Amount Paid: ₦{payment['amount']:,.2f}\n")
        file.write(f"Total Fees: ₦{student['fees']:,.2f}\n")
        file.write(f"Total Paid: ₦{total_paid:,.2f}\n")
        file.write(f"Balance: ₦{balance:,.2f}\n")
        file.write("=" * 35 + "\n")
        file.write("Thank you for your payment.\n")

    print(f"Receipt saved to: {filename}")


# Display student payment information
def view_student(students):
    student_id = input("Enter student ID: ")

    if student_id not in students:
        print("Student not found.")
        return

    student = students[student_id]

    total_paid = sum(
        p["amount"] for p in student["payments"]
    )

    balance = student["fees"] - total_paid

    print("\n--- STUDENT FEE REPORT ---")
    print(f"Student: {student['name']}")
    print(f"Parent: {student['parent']}")
    print(f"Total Fees: ₦{student['fees']:,.2f}")
    print(f"Total Paid: ₦{total_paid:,.2f}")
    print(f"Outstanding Balance: ₦{balance:,.2f}")

    if balance == 0:
        print("Status: FULLY PAID")
    else:
        print("Status: PAYMENT OUTSTANDING")


# Generate a payment reminder
def generate_reminder(students):
    student_id = input("Enter student ID: ")

    if student_id not in students:
        print("Student not found.")
        return

    student = students[student_id]

    total_paid = sum(
        p["amount"] for p in student["payments"]
    )

    balance = student["fees"] - total_paid

    if balance <= 0:
        print("This student has no outstanding fees.")
        return

    message = f"""
Dear {student['parent']},

This is a friendly reminder from the school regarding
the outstanding school fees for {student['name']}.

Total School Fees: ₦{student['fees']:,.2f}
Total Amount Paid: ₦{total_paid:,.2f}
Outstanding Balance: ₦{balance:,.2f}

Kindly arrange to pay the outstanding balance.

Thank you for your cooperation.

School Management
"""

    os.makedirs("reminders", exist_ok=True)

    filename = os.path.join(
        "reminders", f"{student_id}_reminder.txt"
    )

    with open(filename, "w") as file:
        file.write(message.strip())

    print(message)
    print(f"Reminder saved to: {filename}")


# Main program
def main():
    students = load_students()

    while True:
        print("\n===== STUDENT FEE TRACKER =====")
        print("1. Register Student")
        print("2. Record Payment")
        print("3. View Student Balance")
        print("4. Generate Payment Reminder")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            register_student(students)

        elif choice == "2":
            record_payment(students)

        elif choice == "3":
            view_student(students)

        elif choice == "4":
            generate_reminder(students)

        elif choice == "5":
            print("Thank you for using the system.")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()