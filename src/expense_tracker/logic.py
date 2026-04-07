from datetime import datetime


def is_valid_date(text):
    """Return True if text is a valid date in YYYY-MM-DD format."""
    try:
        datetime.strptime(text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def parse_amount(text):
    """Convert text to a positive float rounded to 2 decimals, or return None."""
    try:
        amount = float(text)
    except ValueError:
        return None

    if amount <= 0:
        return None

    return round(amount, 2)


def get_category_by_choice(choice, categories):
    """Return category key by numeric choice, or None if choice is invalid."""
    if not choice.isdigit():
        return None

    index = int(choice)

    if 1 <= index <= len(categories):
        return categories[index - 1]

    return None


def build_expense(expense_date, amount, category, description):
    """Build and return one expense record as a dictionary."""
    return {
        "date": expense_date,
        "amount": amount,
        "category": category,
        "description": description,
    }


def sum_total(expenses):
    """Return total amount for all given expenses."""
    total = 0

    for expense in expenses:
        total += expense["amount"]

    return round(total, 2)


def filter_by_month(expenses, year, month):
    """Return only expenses that belong to the given year and month."""
    filtered_expenses = []

    for expense in expenses:
        expense_date = datetime.strptime(expense["date"], "%Y-%m-%d")

        if expense_date.year == year and expense_date.month == month:
            filtered_expenses.append(expense)
    return filtered_expenses


def get_available_months(expenses):
    """Return sorted unique months in YYYY-MM format."""
    months = set()

    for expense in expenses:
        expense_date = datetime.strptime(expense["date"], "%Y-%m-%d")
        months.add(expense_date.strftime("%Y-%m"))

    return sorted(months)


def sum_by_category(expenses):
    """Return totals grouped by category key."""
    totals = {}

    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]

    return {category: round(total, 2) for category, total in totals.items()}
