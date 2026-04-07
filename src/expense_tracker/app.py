from datetime import date

from constants import CATEGORY_KEYS, UI_LENGTH
from logic import (
    build_expense,
    get_category_by_choice,
    is_valid_date,
    parse_amount,
    sum_total,
)
from storage import load_expenses, save_expenses
from ui_text import UI, CATEGORY_LABELS, LANG_SELECTION


def choose_language():
    """Ask the user to select the UI language."""
    while True:
        print("\n" + "=" * UI_LENGTH)
        print(f"{LANG_SELECTION['title']['en']} | {LANG_SELECTION['title']['lv']}")
        print("=" * UI_LENGTH)

        for key, labels in LANG_SELECTION["options"].items():
            print(f"{key}) {labels['en']}")

        choice = input(
            f"{LANG_SELECTION['prompt']['en']} | {LANG_SELECTION['prompt']['lv']}: "
        ).strip()

        if choice == "1":
            return "en"
        if choice == "2":
            return "lv"

        print(f"{LANG_SELECTION['error']['en']} | {LANG_SELECTION['error']['lv']}")


def show_menu(ui):
    """Display the main menu and return the user's choice."""
    print("\n" + "=" * UI_LENGTH)
    print(ui["title"])
    print("=" * UI_LENGTH)

    for key, label in ui["commands"].items():
        print(f"{key}) {label}")

    return input(f"{ui['menu_prompt']}: ").strip()


def prompt_date(ui):
    """Ask for a date; use today's date if left empty."""
    default_date = date.today().strftime("%Y-%m-%d")

    while True:
        user_input = input(f"{ui['date_prompt']} [{default_date}]: ").strip()

        if user_input == "":
            return default_date

        if is_valid_date(user_input):
            return user_input

        print(ui["date_error"])


def prompt_category(ui, language):
    """Display localized categories and let the user choose one."""
    print(ui["category_label"])

    labels = CATEGORY_LABELS[language]

    for index, category_key in enumerate(CATEGORY_KEYS, start=1):
        print(f" {index}) {labels[category_key]}")

    while True:
        choice = input(f"{ui['category_prompt']} (1-{len(CATEGORY_KEYS)}): ").strip()
        category_key = get_category_by_choice(choice, CATEGORY_KEYS)

        if category_key is not None:
            return category_key

        print(ui["category_error"])


def prompt_amount(ui):
    """Ask for an amount and validate it."""
    while True:
        user_input = input(f"{ui['amount_prompt']}: ").strip()
        amount = parse_amount(user_input)

        if amount is not None:
            return amount

        print(ui["amount_error"])


def prompt_description(ui):
    """Ask for an expense description."""
    return input(f"{ui['description_prompt']}: ").strip()


def add_expense_ui(ui, language):
    """Load fresh data, collect input, add expense, and save it."""
    expenses = load_expenses()

    expense_date = prompt_date(ui)
    category = prompt_category(ui, language)
    amount = prompt_amount(ui)
    description = prompt_description(ui)

    expense = build_expense(
        expense_date=expense_date,
        amount=amount,
        category=category,
        description=description,
    )

    expenses.append(expense)
    save_expenses(expenses)

    print(
        f"{ui['added_label']}: "
        f"{expense['date']} | "
        f"{CATEGORY_LABELS[language][expense['category']]} | "
        f"{expense['amount']:.2f} EUR | "
        f"{expense['description']}"
    )


def show_expenses_ui(ui, language):
    """Load fresh data and display all expenses in a formatted table."""
    expenses = load_expenses()

    if not expenses:
        print(f"\n{ui['no_expenses']}")
        return

    headers = ui["table_headers"]

    print()
    print(f"{headers[0]:<12} {headers[1]:>10} {headers[2]:<22} {headers[3]}")
    print("-" * UI_LENGTH)

    for expense in expenses:
        category_label = CATEGORY_LABELS[language].get(
            expense["category"], expense["category"]
        )

        print(
            f"{expense['date']:<12} "
            f"{expense['amount']:>8.2f} EUR "
            f"{category_label:<22} "
            f"{expense['description']}"
        )

    print("-" * UI_LENGTH)
    print(
        f"{ui['total_label']}: {sum_total(expenses):.2f} EUR ({len(expenses)} {ui['records_label']})"
    )


def handle_choice(choice, ui, language):
    """Execute action based on menu choice."""
    if choice == "1":
        add_expense_ui(ui, language)
        return True

    if choice == "2":
        show_expenses_ui(ui, language)
        return True

    if choice == "7":
        print(ui["goodbye"])
        return False

    print(ui["invalid_choice"])
    return True


def main():
    """Run the main application loop."""
    language = choose_language()
    ui = UI[language]

    is_running = True
    while is_running:
        choice = show_menu(ui)
        is_running = handle_choice(choice, ui, language)


if __name__ == "__main__":
    main()
