import json
from pathlib import Path


FILEPATH = Path(__file__).resolve().parent / "expenses.json"


def load_expenses():
    """Load expenses from JSON file. Return empty list if file is missing or empty."""
    if not FILEPATH.exists():
        return []

    with open(FILEPATH, "r", encoding="utf-8") as file:
        content = file.read().strip()

        if not content:
            return []

        return json.loads(content)


def save_expenses(expenses):
    """Save expenses list to JSON file."""
    with open(FILEPATH, "w", encoding="utf-8") as file:
        json.dump(expenses, file, ensure_ascii=False, indent=2)
