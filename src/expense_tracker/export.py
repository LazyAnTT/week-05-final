import csv


def export_to_csv(expenses, filepath):
    """Export expenses to a CSV file with English headers."""
    with open(filepath, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)

        writer.writerow(["Date", "Amount", "Category", "Description"])

        for expense in expenses:
            writer.writerow(
                [
                    expense["date"],
                    f"{expense['amount']:.2f}",
                    expense["category"],
                    expense["description"],
                ]
            )
