
## A. Program description

- Expense Tracker is a Python command-line application for recording and analyzing personal expenses.  
- The user can add expenses, view all saved records, filter them by month, see totals by category, delete records, and export data to CSV.  
- All data is stored in a JSON file so it remains available between program runs.

## B. Data structure

One expense will be stored as a dictionary inside a list.

Example:
 [
    {
        "date": "2025-02-15",
        "amount": 12.50,
        "category": "Ēdiens",
        "description": "Pusdienas kafejnīcā"
    },
    {
        "date": "2025-02-16",
        "amount": 3.40,
        "category": "Transports",
        "description": "Autobusa biļete"
    }
]

Why? 
- each expense is one separate record
- dictionaries make field names clear (date, amount, category, description)
- the structure is easy to save in JSON
- it is convenient for filtering, grouping, and summing later


## C. Module plan

1. expense_tracker/app.py

Main CLI program.
Responsible for:

- showing the menu
- reading user input
- validating input before passing data forward
- calling functions from other modules
- printing formatted output in terminal

2. expense_tracker/storage.py

Handles JSON file operations only.

Planned functions:

- load_expenses() — reads expenses.json; if file does not exist, returns empty list
- save_expenses(expenses) — saves expenses list into JSON using ensure_ascii=False

3. expense_tracker/logic.py
Planned functions:

- sum_total(expenses) — returns total sum of given expenses
- filter_by_month(expenses, year, month) — returns only expenses from selected month
- sum_by_category(expenses) — returns dictionary with totals grouped by category
- get_available_months(expenses) — returns unique list of available months 

4. expense_tracker/export.py

Handles CSV export.

Planned functions:

export_to_csv(expenses, filepath) — writes expenses to CSv

5. expense_tracker/expenses.json

Stores all saved expense data.

6. docs/plan.md

Contains the planning document for step 1.

7. docs/DEVLOG.md

Contains development notes about progress, problems, and solutions.

8. README.md

Contains project description, setup instructions, usage, and author info.

## D. User scenarios
Scenario 1 — adding a valid expense

User opens the program and chooses “Add expense”.
The program asks for date, category, amount, and description.
The user enters valid values.
The program saves the new expense to expenses.json and prints a success message.

Scenario 2 — entering invalid amount

User chooses “Add expense”.
The user enters text or a negative number instead of a valid amount.
The program shows an error message such as “Amount must be a positive number” and asks again.

Scenario 3 — filtering by month

User chooses “Filter by month”.
The program shows available months based on saved data.
The user selects one month.
The program prints only expenses from that month and shows total amount for the filtered results.

*** There can be many scenarios. Will try to cover them with tests. 

## E. Edge cases
1. expenses.json does not exist

The program should not crash.
load_expenses() should return an empty list, and the file can be created later when the first expense is saved.

2. Empty expense list

If there are no expenses and the user chooses “Show expenses”, the program should print a clear message like:
Nav izdevumu.

If the user chooses delete on an empty list, the program should show a message and return safely.

*** There can be many scenarios. Will try to cover them with tests. 
