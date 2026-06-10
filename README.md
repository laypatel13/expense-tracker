# 💰 Expense Tracker - CLI

A simple command-line Expense Tracker built using Python.
This project helps you record, view, and summarize your daily expenses with a colorful and neatly formatted tabular interface.

---

## ✨ Features

- Add expenses with amount, category, and date
- View all recorded expenses in a tabular format
- Get category-wise summary and total spending
- Save data in a JSON file (`expenses.json`)
- Reset all expenses when needed
- Colorful CLI output for better readability

---

## 📦 Install via pip

```bash
pip install laypatel13-expense-tracker
```

Then run it from anywhere in your terminal:

```bash
expense-tracker
```

---

## 🛠️ Install from source

```bash
git clone https://github.com/laypatel13/expense-tracker.git
cd expense-tracker
pip install -r requirements.txt
pip install -e .
```

Then run:

```bash
expense-tracker
```

---

## 📂 Project Structure

```text
expense-tracker/
├── expense_tracker/
│   ├── __init__.py
│   └── main.py
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## 🧰 Built With

- Used [Colorama](https://pypi.org/project/colorama/) for colored terminal output.
- Used [Tabulate](https://pypi.org/project/tabulate/) for formatted table display.
