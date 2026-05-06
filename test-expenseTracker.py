import pytest
from unittest.mock import patch, mock_open
import json

import expenseTracker

@pytest.fixture(autouse=True)
def reset_data():
    """Reset the global data before and after each test."""
    expenseTracker.data = []
    expenseTracker.totals = {}
    yield
    expenseTracker.data = []
    expenseTracker.totals = {}

def test_load_expenses_file_not_exists():
    with patch("os.path.exists", return_value=False):
        assert expenseTracker.load_expenses() == []

def test_load_expenses_file_exists_empty():
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=" ")):
            assert expenseTracker.load_expenses() == []

def test_load_expenses_file_exists_with_data():
    mock_data = [{"amount": 100, "category": "Food", "date": "2023-01-01"}]
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
            assert expenseTracker.load_expenses() == mock_data

def test_add_expense_valid(capsys):
    inputs = ["100", "Food", "2023-01-01", "quit"]
    with patch("builtins.input", side_effect=inputs):
        expenseTracker.add_expense()
    
    assert len(expenseTracker.data) == 1
    assert expenseTracker.data[0] == {"amount": 100, "category": "Food", "date": "2023-01-01"}
    
    captured = capsys.readouterr()
    assert "Expense added successfully!" in captured.out

def test_add_expense_invalid_amount(capsys):
    inputs = ["invalid", "100", "Food", "2023-01-01", "quit"]
    with patch("builtins.input", side_effect=inputs):
        expenseTracker.add_expense()
    
    assert len(expenseTracker.data) == 1
    captured = capsys.readouterr()
    assert "Invalid amount. Please enter a number." in captured.out
    assert "Expense added successfully!" in captured.out

def test_save_expense():
    expenseTracker.data = [{"amount": 100, "category": "Food", "date": "2023-01-01"}]
    m_open = mock_open()
    with patch("builtins.open", m_open):
        expenseTracker.save_expense()
    
    m_open.assert_called_once_with("expenses.json", "w")
    handle = m_open()
    written_content = "".join(call.args[0] for call in handle.write.call_args_list)
    assert json.loads(written_content) == expenseTracker.data

def test_view_expenses_empty(capsys):
    expenseTracker.data = []
    expenseTracker.view_expenses()
    captured = capsys.readouterr()
    assert "No expenses recorded yet." in captured.out

def test_view_expenses_with_data(capsys):
    expenseTracker.data = [{"amount": 100, "category": "Food", "date": "2023-01-01"}]
    expenseTracker.view_expenses()
    captured = capsys.readouterr()
    assert "--- Your Expenses ---" in captured.out
    assert "Food" in captured.out
    assert "100" in captured.out
    assert "2023-01-01" in captured.out

def test_summary_empty(capsys):
    expenseTracker.data = []
    expenseTracker.summary()
    captured = capsys.readouterr()
    assert "No expenses to summarize." in captured.out

def test_summary_with_data(capsys):
    expenseTracker.data = [
        {"amount": 100, "category": "Food", "date": "2023-01-01"},
        {"amount": 50, "category": "Food", "date": "2023-01-02"},
        {"amount": 200, "category": "Rent", "date": "2023-01-03"},
    ]
    expenseTracker.summary()
    captured = capsys.readouterr()
    assert "--- Expense Summary ---" in captured.out
    assert "Food" in captured.out
    assert "150" in captured.out
    assert "Rent" in captured.out
    assert "200" in captured.out
    assert "350" in captured.out # Total

def test_reset_expenses_yes(capsys):
    expenseTracker.data = [{"amount": 100, "category": "Food", "date": "2023-01-01"}]
    with patch("builtins.input", return_value="yes"):
        with patch("expenseTracker.save_expense") as mock_save:
            expenseTracker.reset_expenses()
            assert expenseTracker.data == []
            mock_save.assert_called_once()
            
    captured = capsys.readouterr()
    assert "All expenses cleared!" in captured.out

def test_reset_expenses_no(capsys):
    expenseTracker.data = [{"amount": 100, "category": "Food", "date": "2023-01-01"}]
    with patch("builtins.input", return_value="no"):
        with patch("expenseTracker.save_expense") as mock_save:
            expenseTracker.reset_expenses()
            assert len(expenseTracker.data) == 1
            mock_save.assert_not_called()
            
    captured = capsys.readouterr()
    assert "Reset cancelled." in captured.out

def test_main_quit():
    with patch("expenseTracker.load_expenses", return_value=[]):
        with patch("builtins.input", return_value="4"):
            expenseTracker.main()
