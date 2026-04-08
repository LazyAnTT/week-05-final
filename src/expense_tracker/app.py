from datetime import date

from constants import CATEGORY_KEYS, UI_LENGTH
from logic import (
    build_expense,
    get_category_by_choice,
    is_valid_date,
    parse_amount,
    sum_total,
    filter_by_month,
    get_available_months,
    sum_by_category,
    format_choice_error,
)
from export import export_to_csv
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


def show_expenses_list(expenses, ui, language):
    """Display a given list of expenses in a formatted table."""
    if not expenses:
        print(f"\n{ui['no_expenses']}")
        return

    headers = ui["table_headers"]

    print()
    print(f"{headers[0]:<12} {headers[1]:<8} {headers[2]:<18} {headers[3]:<15}")
    print("-" * UI_LENGTH)

    for expense in expenses:
        category_label = CATEGORY_LABELS[language].get(
            expense["category"], expense["category"]
        )

        print(
            f"{expense['date']:<12} "
            f"{expense['amount']:<8.2f} EUR "
            f"{category_label:<18} "
            f"{expense['description']}"
        )

    print("-" * UI_LENGTH)
    print(
        f"{ui['total_label']}: {sum_total(expenses):.2f} EUR "
        f"({len(expenses)} {ui['records_label']})"
    )


def show_expenses_ui(ui, language):
    """Load fresh data and display all expenses in a formatted table."""
    expenses = load_expenses()
    show_expenses_list(expenses, ui, language)


def prompt_month_choice(ui, months):
    """Ask the user to choose one month from the available list."""
    valid_choices = [str(index) for index in range(1, len(months) + 1)]

    while True:
        user_input = input(f"{ui['choose_month_prompt']} (1-{len(months)}): ").strip()

        if not user_input.isdigit():
            print(format_choice_error(ui, valid_choices))
            continue

        month_index = int(user_input)

        if 1 <= month_index <= len(months):
            return months[month_index - 1]

        print(format_choice_error(ui, valid_choices))


def filter_expenses_ui(ui, language):
    """Load expenses, let the user choose a month, and show filtered results."""
    expenses = load_expenses()
    months = get_available_months(expenses)

    if not months:
        print(f"\n{ui['no_months']}")
        return

    print(f"\n{ui['available_months_label']}:")
    for index, month in enumerate(months, start=1):
        print(f"{index}) {month}")

    selected_month = prompt_month_choice(ui, months)
    year_text, month_text = selected_month.split("-")

    filtered_expenses = filter_by_month(
        expenses,
        year=int(year_text),
        month=int(month_text),
    )
    show_expenses_list(filtered_expenses, ui, language)


def show_category_summary_ui(ui, language):
    """Show totals grouped by category."""
    expenses = load_expenses()

    if not expenses:
        print(f"\n{ui['no_expenses']}")
        return

    category_totals = sum_by_category(expenses)

    print(f"\n{ui['category_summary_label']}:")
    print("-" * UI_LENGTH)

    for category_key, total in category_totals.items():
        category_label = CATEGORY_LABELS[language].get(category_key, category_key)

        print(f"{category_label:<22} {total:>8.2f} EUR")

    print("-" * UI_LENGTH)
    print(f"{ui['total_label']}: {sum_total(expenses):.2f} EUR")


def delete_expense_ui(ui, language):
    """Load fresh data, show expenses with temporary numbers, and delete one item."""
    expenses = load_expenses()

    if not expenses:
        print(f"\n{ui['no_expenses']}")
        return

    headers = ui["table_headers"]

    print()
    print(
        f"{ui['expense_number_header']:<4} "
        f"{headers[0]:<12} "
        f"{headers[1]:>10} "
        f"{headers[2]:<22} "
        f"{headers[3]}"
    )
    print("-" * UI_LENGTH)

    for index, expense in enumerate(expenses, start=1):
        category_label = CATEGORY_LABELS[language].get(
            expense["category"], expense["category"]
        )

        print(
            f"{index:<4} "
            f"{expense['date']:<12} "
            f"{expense['amount']:>8.2f} EUR "
            f"{category_label:<22} "
            f"{expense['description']}"
        )

    print("-" * UI_LENGTH)

    while True:
        user_input = input(f"{ui['delete_prompt']}: ").strip()

        if not user_input.isdigit():
            print(ui["delete_error"])
            continue

        selected_index = int(user_input)

        if selected_index == 0:
            print(ui["delete_cancelled"])
            return

        if 1 <= selected_index <= len(expenses):
            deleted_expense = expenses.pop(selected_index - 1)
            save_expenses(expenses)

            category_label = CATEGORY_LABELS[language].get(
                deleted_expense["category"],
                deleted_expense["category"],
            )

            print(
                f"{ui['delete_success']}: "
                f"{deleted_expense['date']} | "
                f"{category_label} | "
                f"{deleted_expense['amount']:.2f} EUR | "
                f"{deleted_expense['description']}"
            )
            return

        print(ui["delete_error"])


def export_csv_ui(ui):
    """Load fresh data and export expenses to a CSV file."""
    expenses = load_expenses()

    default_filename = ui["export_default_filename"]

    user_input = input(f"{ui['export_prompt']} [{default_filename}]: ").strip()

    if user_input == "":
        filename = default_filename
    else:
        filename = user_input

    if not filename.lower().endswith(".csv"):
        filename += ".csv"

    export_to_csv(expenses, filename)

    print(f"{ui['export_success']}: {len(expenses)} -> {filename}")


def handle_choice(choice, ui, language):
    """Execute action based on menu choice."""
    CONTINUE = True
    EXIT = False

    if choice == "1":
        add_expense_ui(ui, language)
        return CONTINUE

    if choice == "2":
        show_expenses_ui(ui, language)
        return CONTINUE

    if choice == "3":
        filter_expenses_ui(ui, language)
        return CONTINUE

    if choice == "4":
        show_category_summary_ui(ui, language)
        return CONTINUE

    if choice == "5":
        delete_expense_ui(ui, language)
        return True

    if choice == "6":
        export_csv_ui(ui)
        return CONTINUE

    if choice == "7":
        print(ui["goodbye"])
        return EXIT

    valid_choices = list(ui["commands"].keys())
    print(format_choice_error(ui, valid_choices))
    return CONTINUE


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
