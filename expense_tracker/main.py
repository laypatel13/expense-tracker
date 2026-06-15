import json
import os
from colorama import init, Fore, Back, Style
from tabulate import tabulate

init(autoreset=True)

data = []
totals = {}

def load_expenses():
    if os.path.exists("expenses.json"):
        try:
            with open("expenses.json", "r") as f:
                content = f.read()
                if content.strip() == "":
                    return []
                return json.loads(content)
        except (json.JSONDecodeError, IOError) as e:
            print(Fore.WHITE + Back.RED + f"Fatal Error: Failed to load expenses. {e}" + Style.RESET_ALL)
            return []
    return []

def add_expense():
    while True:
        amount_input = input(Fore.WHITE + Style.NORMAL + "Enter Amount Of Expense (or 'quit' to finish): " + Style.RESET_ALL)
        if amount_input.lower() == 'quit':
            break
        try:
            amount = int(amount_input)
            category = input(Fore.WHITE + Style.NORMAL + "Enter Category Of Expense: " + Style.RESET_ALL)
            date = input(Fore.WHITE + Style.NORMAL + "Enter Date Of Expense (DD-MM-YYYY): " + Style.RESET_ALL)
            new_entry = {"amount": amount, "category": category, "date": date,}
            data.append(new_entry)
            print(Fore.GREEN + Back.BLACK + Style.BRIGHT + "Expense Added Successfully!" + Style.RESET_ALL + "\n")
        except ValueError:
            print(Fore.RED + Style.BRIGHT + "Invalid Amount. Please Enter a Number." + Style.RESET_ALL + "\n")


def save_expense():
    try:
        with open("expenses.json", "w") as f:
            json.dump(data, f)
    except IOError as e:
        print(Fore.WHITE + Back.RED + f"Fatal Error: Failed to save expenses. {e}" + Style.RESET_ALL)

def view_expenses():
    if not data:
        print(Fore.WHITE + Back.BLACK + Style.BRIGHT + "No Expenses Recorded Yet." + Style.RESET_ALL)
        return
    print("\n" + Fore.BLACK + Back.WHITE + "--- Your Expenses ---" + Style.RESET_ALL)
    table_data = []
    for expense in data:
        table_data.append([
            Fore.WHITE + Style.BRIGHT + expense['date'] + Style.RESET_ALL,
            Fore.WHITE + Style.BRIGHT + expense['category'] + Style.RESET_ALL,
            Fore.WHITE + Style.BRIGHT + f"{expense['amount']}" + Style.RESET_ALL
        ])
    headers = [Style.BRIGHT + "Date" + Style.RESET_ALL, Style.BRIGHT + "Category" + Style.RESET_ALL, Style.BRIGHT + "Amount" + Style.RESET_ALL]
    print(tabulate(table_data, headers=headers, tablefmt="pretty", disable_numparse=True))

def summary():
    if not data:
        print(Fore.WHITE + Back.BLACK + Style.BRIGHT + "No Expenses To Summarize." + Style.RESET_ALL)
        return
        
    totals.clear()
    for expense in data:
        category = expense["category"]
        amount = expense["amount"]
        if category in totals:
            totals[category] += amount   
        else:
            totals[category] = amount    
            
    print("\n" + Fore.BLACK + Back.WHITE + "--- Expense Summary ---" + Style.RESET_ALL)
    table_data = []
    for category, total in totals.items():
        table_data.append([
            Fore.WHITE + Style.DIM + f"{category}" + Style.RESET_ALL,
            Fore.WHITE + Style.DIM + f"{total}" + Style.RESET_ALL
        ])

    table_data.append([
        Fore.WHITE + Style.NORMAL + "Total Expense Done!" + Style.RESET_ALL,
        Fore.WHITE + Style.NORMAL + f"{sum(totals.values())}" + Style.RESET_ALL
    ])

    headers = [Style.BRIGHT + "Category" + Style.RESET_ALL, Style.BRIGHT + "Total Amount" + Style.RESET_ALL]
    print(tabulate(table_data, headers=headers, tablefmt="pretty", disable_numparse=True))

def reset_expenses():
    global data
    confirm = input(Fore.RED + Style.BRIGHT + "Are You Sure You Want To Reset All Expenses? (yes/no): " + Style.RESET_ALL)
    if confirm.lower() == "yes":
        data = []
        save_expense()
        print(Fore.GREEN + Back.BLACK + "All Expenses Cleared!" + Style.RESET_ALL)
    else:
        print(Fore.RED + Style.NORMAL + "Reset Cancelled." + Style.RESET_ALL)

def main():
    global data
    data = load_expenses()     

    while True:                 
        print("\n" + Fore.BLACK + Back.WHITE + "--- Expense Tracker ---" + Style.RESET_ALL)
        print(Fore.YELLOW + Style.NORMAL + "(1) Add New Expense" + Style.RESET_ALL)
        print(Fore.YELLOW + Style.NORMAL + "(2) View Expenses" + Style.RESET_ALL)
        print(Fore.YELLOW + Style.NORMAL + "(3) View Summary Of Expenses" + Style.RESET_ALL)
        print(Fore.YELLOW + Style.NORMAL + "(4) Quit Expense Tracker" + Style.RESET_ALL)
        print(Fore.YELLOW + Style.NORMAL + "(5) Reset Expenses" + Style.RESET_ALL)

        choice = input("\n" + Fore.CYAN + Style.BRIGHT + "Enter Your Choice: " + Style.RESET_ALL)

        if choice == "1":
            add_expense()
            save_expense() 
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            summary()
        elif choice == "4":
            print(Fore.WHITE + Style.BRIGHT + "Bye! Thanks For Using The Expense Tracker.!" + Style.RESET_ALL)
            break  
        elif choice == "5":
            reset_expenses()          
        else:
            print(Fore.RED + Style.BRIGHT + "Invalid choice, try again!" + Style.RESET_ALL)

if __name__ == "__main__":
    main()