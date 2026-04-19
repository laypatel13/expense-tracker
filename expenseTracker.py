import json
import os

data = []
totals = {}

def load_expenses():
    if os.path.exists("expenses.json"):
        with open("expenses.json", "r") as f:
            content = f.read()
            if content.strip() == "":
                return []
            return json.loads(content)
    return []

def add_expense():
    while True:
        amount_input = input("Enter amount (or 'quit' to finish): ")
        if amount_input.lower() == 'quit':
            break
        try:
            amount = int(amount_input)
            category = input("Enter category: ")
            date = input("Enter date (YYYY-MM-DD): ")
            new_entry = {"amount": amount, "category": category, "date": date,}
            data.append(new_entry)
        except ValueError:
            print("Invalid amount. Please enter a number.")


def save_expense():
    with open("expenses.json", "w") as f:
        json.dump(data, f)

def view_expenses():
    for expense in data:
        print(expense["date"], "|", expense["category"], "|",  expense["amount"])

def summary():
    for expense in data:
        category = expense["category"]
        amount = expense["amount"]
        if category in totals:
            totals[category] += amount   
        else:
            totals[category] = amount    
    for category, total in totals.items():
        print(category, "→", total)

    print("Total →", sum(totals.values()))

def reset_expenses():
    global data
    confirm = input("Are you sure you want to reset all expenses? (yes/no): ")
    if confirm.lower() == "yes":
        data = []
        save_expense()
        print("All expenses cleared!")
    else:
        print("Reset cancelled.")

def main():
    global data
    data = load_expenses()     

    while True:                 
        print("\n--- Expense Tracker ---")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Summary")
        print("4. Quit")
        print("5. Reset")

        choice = input("Enter choice: ")

        if choice == "1":
            add_expense()
            save_expense() 
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            summary()
        elif choice == "4":
            print("Bye!")
            break  
        elif choice == "5":
            reset_expenses()          
        else:
            print("Invalid choice, try again!")

main()