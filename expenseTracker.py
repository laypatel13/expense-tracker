import json
import os

def load_expenses():
    if os.path.exists("expenses.json"):
        with open("expenses.json", "r") as f:
            content = f.read()
            if content.strip() == "":
                return []
            return json.loads(content)
    return []

def add_expense():
    pass

def save_expense():
    pass

def view_expenses():
    pass
