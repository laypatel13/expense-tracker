import pytest
from unittest.mock import patch, mock_open
import json

from expense_tracker import main as et

@pytest.fixture(autouse=True)
def reset_data():
    et.data = []
    et.totals = {}
    yield
    et.data = []
    et.totals = {}

def test_load_expenses_file_not_exists():
    with patch("os.path.exists", return_value=False):
        assert et.load_expenses() == []

def test_load_expenses_file_exists_empty():
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=" ")):
            assert et.load_expenses() == []

def test_load_expenses_file_exists_with_data():
    mock_data = [{"amount": 100, "category": "Food", "date": "2023-01-01"}]
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
            assert et.load_expenses() == mock_data

def test_add_expense_valid(capsys):
    inputs = ["100", "Food", "2023-01-01", "quit"]
    with patch("builtins.input", side_effect=inputs):
        et.add_expense()
    assert len(et.data) == 1
    assert et.data[0] == {"amount": 100, "category": "Food", "date": "2023-01-01"}
    captured = capsys.readouterr()
    assert "Expense Added Successfully!" in captured.out

def test_add_expense_invalid_amount(capsys):
    inputs = ["invalid", "100", "Food", "2023-01-01", "quit"]
    with patch("builtins.input", side_effect=inputs):
        et.add_expense()
    assert len(et.data) == 1
    captured = capsys.readouterr()
    assert "Invalid Amount" in captured.out
    assert "Expense Added Successfully!" in captured.out

def test_save_expense():
    et.data = [{"amount": 100, "category": "Food", "date": "2023-01-01"}]
    m_open = mock_open()
    with patch("builtins.open", m_open):
        et.save_expense()
    m_open.assert_called_once_with("expenses.json", "w")
    handle = m_open()
    written_content = "".join(call.args[0] for call in handle.write.call_args_list)
    assert json.loads(written_content) == et.data

def test_view_expenses_empty(capsys):
    et.data = []
    et.view_expenses()
    captured = capsys.readouterr()
    assert "No Expenses Recorded Yet." in captured.out

def test_view_expenses_with_data(capsys):
    et.data = [{"amount": 100, "category": "Food", "date": "2023-01-01"}]
    et.view_expenses()
    captured = capsys.readouterr()
    assert "--- Your Expenses ---" in captured.out
    assert "Food" in captured.out
    assert "100" in captured.out
    assert "2023-01-01" in captured.out

def test_summary_empty(capsys):
    et.data = []
    et.summary()
    captured = capsys.readouterr()
    assert "No Expenses To Summarize." in captured.out

def test_summary_with_data(capsys):
    et.data = [
        {"amount": 100, "category": "Food", "date": "2023-01-01"},
        {"amount": 50,  "category": "Food", "date": "2023-01-02"},
        {"amount": 200, "category": "Rent", "date": "2023-01-03"},
    ]
    et.summary()
    captured = capsys.readouterr()
    assert "--- Expense Summary ---" in captured.out
    assert "Food" in captured.out
    assert "150" in captured.out
    assert "Rent" in captured.out
    assert "200" in captured.out
    assert "350" in captured.out

def test_reset_expenses_yes(capsys):
    et.data = [{"amount": 100, "category": "Food", "date": "2023-01-01"}]
    with patch("builtins.input", return_value="yes"):
        with patch("expense_tracker.main.save_expense") as mock_save:
            et.reset_expenses()
            assert et.data == []
            mock_save.assert_called_once()
    captured = capsys.readouterr()
    assert "All Expenses Cleared!" in captured.out

def test_reset_expenses_no(capsys):
    et.data = [{"amount": 100, "category": "Food", "date": "2023-01-01"}]
    with patch("builtins.input", return_value="no"):
        with patch("expense_tracker.main.save_expense") as mock_save:
            et.reset_expenses()
            assert len(et.data) == 1
            mock_save.assert_not_called()
    captured = capsys.readouterr()
    assert "Reset Cancelled." in captured.out

def test_main_quit():
    with patch("expense_tracker.main.load_expenses", return_value=[]):
        with patch("builtins.input", return_value="4"):
            et.main()