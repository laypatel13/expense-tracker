import json
import os

data = []

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
        print(expense["date"] | expense["category"] | expense["amount"])
