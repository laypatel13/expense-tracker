import json
import os
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

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
        amount_input = input(Fore.CYAN + "Enter amount (or 'quit' to finish): " + Style.RESET_ALL)
        if amount_input.lower() == 'quit':
            break
        try:
            amount = int(amount_input)
            category = input(Fore.CYAN + "Enter category: " + Style.RESET_ALL)
            date = input(Fore.CYAN + "Enter date (YYYY-MM-DD): " + Style.RESET_ALL)
            new_entry = {"amount": amount, "category": category, "date": date,}
            data.append(new_entry)
            print(Fore.GREEN + "Expense added successfully!\n" + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid amount. Please enter a number.\n" + Style.RESET_ALL)


def save_expense():
    with open("expenses.json", "w") as f:
        json.dump(data, f)

def view_expenses():
    if not data:
        print(Fore.YELLOW + "No expenses recorded yet." + Style.RESET_ALL)
        return
    print(Fore.MAGENTA + Style.BRIGHT + "\n--- Your Expenses ---" + Style.RESET_ALL)
    for expense in data:
        print(Fore.GREEN + f"{expense['date']}" + Style.RESET_ALL + " | " + Fore.YELLOW + f"{expense['category']}" + Style.RESET_ALL + " | " + Fore.CYAN + f"${expense['amount']}" + Style.RESET_ALL)

def summary():
    if not data:
        print(Fore.YELLOW + "No expenses to summarize." + Style.RESET_ALL)
        return
        
    totals.clear()
    for expense in data:
        category = expense["category"]
        amount = expense["amount"]
        if category in totals:
            totals[category] += amount   
        else:
            totals[category] = amount    
            
    print(Fore.MAGENTA + Style.BRIGHT + "\n--- Expense Summary ---" + Style.RESET_ALL)
    for category, total in totals.items():
        print(Fore.YELLOW + f"{category}" + Style.RESET_ALL + " → " + Fore.CYAN + f"${total}" + Style.RESET_ALL)

    print(Fore.GREEN + Style.BRIGHT + f"Total → {sum(totals.values())}" + Style.RESET_ALL)

def reset_expenses():
    global data
    confirm = input(Fore.RED + Style.BRIGHT + "Are you sure you want to reset all expenses? (yes/no): " + Style.RESET_ALL)
    if confirm.lower() == "yes":
        data = []
        save_expense()
        print(Fore.GREEN + "All expenses cleared!" + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "Reset cancelled." + Style.RESET_ALL)

def main():
    global data
    data = load_expenses()     

    while True:                 
        print(Fore.BLUE + Style.BRIGHT + "\n--- Expense Tracker ---" + Style.RESET_ALL)
        print(Fore.YELLOW + "1." + Style.RESET_ALL + " Add Expense")
        print(Fore.YELLOW + "2." + Style.RESET_ALL + " View Expenses")
        print(Fore.YELLOW + "3." + Style.RESET_ALL + " Summary")
        print(Fore.YELLOW + "4." + Style.RESET_ALL + " Quit")
        print(Fore.YELLOW + "5." + Style.RESET_ALL + " Reset")

        choice = input(Fore.CYAN + "\nEnter choice: " + Style.RESET_ALL)

        if choice == "1":
            add_expense()
            save_expense() 
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            summary()
        elif choice == "4":
            print(Fore.MAGENTA + "Bye!" + Style.RESET_ALL)
            break  
        elif choice == "5":
            reset_expenses()          
        else:
            print(Fore.RED + "Invalid choice, try again!" + Style.RESET_ALL)

if __name__ == "__main__":
    main()