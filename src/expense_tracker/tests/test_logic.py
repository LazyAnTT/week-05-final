import unittest

from src.expense_tracker.logic import (
    build_expense,
    get_category_by_choice,
    is_valid_date,
    parse_amount,
    sum_total,
    filter_by_month,
    get_available_months,
)


class TestLogic(unittest.TestCase):
    def test_is_valid_date_returns_true_for_valid_date(self):
        self.assertTrue(is_valid_date("2025-02-15"))

    def test_is_valid_date_returns_false_for_invalid_date(self):
        self.assertFalse(is_valid_date("2025-02-30"))

    def test_is_valid_date_returns_false_for_wrong_format(self):
        self.assertFalse(is_valid_date("15-02-2025"))

    def test_parse_amount_returns_float_for_valid_input(self):
        self.assertEqual(parse_amount("12.50"), 12.50)

    def test_parse_amount_returns_none_for_text(self):
        self.assertIsNone(parse_amount("abc"))

    def test_parse_amount_returns_none_for_negative_number(self):
        self.assertIsNone(parse_amount("-5"))

    def test_parse_amount_returns_none_for_zero(self):
        self.assertIsNone(parse_amount("0"))

    def test_get_category_by_choice_returns_category_key(self):
        categories = ["food", "transport", "other"]
        self.assertEqual(get_category_by_choice("2", categories), "transport")

    def test_get_category_by_choice_returns_none_for_invalid_choice(self):
        categories = ["food", "transport", "other"]
        self.assertIsNone(get_category_by_choice("9", categories))

    def test_build_expense_returns_expected_dictionary(self):
        expense = build_expense(
            expense_date="2025-02-15",
            amount=12.50,
            category="food",
            description="Lunch",
        )

        expected = {
            "date": "2025-02-15",
            "amount": 12.50,
            "category": "food",
            "description": "Lunch",
        }

        self.assertEqual(expense, expected)

    def test_sum_total_returns_correct_sum(self):
        expenses = [
            {
                "date": "2025-02-15",
                "amount": 12.50,
                "category": "food",
                "description": "Lunch",
            },
            {
                "date": "2025-02-16",
                "amount": 3.40,
                "category": "transport",
                "description": "Bus",
            },
        ]

        self.assertEqual(sum_total(expenses), 15.90)

    def test_sum_total_returns_zero_for_empty_list(self):
        self.assertEqual(sum_total([]), 0)

    def test_filter_by_month_returns_only_matching_month(self):
        expenses = [
            {
                "date": "2025-02-15",
                "amount": 12.50,
                "category": "food",
                "description": "Lunch",
            },
            {
                "date": "2025-02-16",
                "amount": 3.40,
                "category": "transport",
                "description": "Bus",
            },
            {
                "date": "2025-03-01",
                "amount": 20.00,
                "category": "shopping",
                "description": "Book",
            },
        ]

        result = filter_by_month(expenses, 2025, 2)

        expected = [
            {
                "date": "2025-02-15",
                "amount": 12.50,
                "category": "food",
                "description": "Lunch",
            },
            {
                "date": "2025-02-16",
                "amount": 3.40,
                "category": "transport",
                "description": "Bus",
            },
        ]

        self.assertEqual(result, expected)

    def test_filter_by_month_returns_empty_list_when_no_matches(self):
        expenses = [
            {
                "date": "2025-02-15",
                "amount": 12.50,
                "category": "food",
                "description": "Lunch",
            }
        ]

        result = filter_by_month(expenses, 2025, 3)

        self.assertEqual(result, [])

    def test_get_available_months_returns_sorted_unique_months(self):
        expenses = [
            {
                "date": "2025-03-01",
                "amount": 20.00,
                "category": "shopping",
                "description": "Book",
            },
            {
                "date": "2025-02-15",
                "amount": 12.50,
                "category": "food",
                "description": "Lunch",
            },
            {
                "date": "2025-02-16",
                "amount": 3.40,
                "category": "transport",
                "description": "Bus",
            },
        ]

        result = get_available_months(expenses)

        self.assertEqual(result, ["2025-02", "2025-03"])

    def test_get_available_months_returns_empty_list_for_no_expenses(self):
        self.assertEqual(get_available_months([]), [])


if __name__ == "__main__":
    unittest.main()
