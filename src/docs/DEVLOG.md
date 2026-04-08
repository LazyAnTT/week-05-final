# Development Journal(logs)

## 1. Step - Planning
- MVC model - file responsability distribution
- Understanding the scope, data structures and functionality of the application
- Figuring out what can be reused from week-04 project

# 2. Core functioanlity

Implemented core CLI functionality: add expense, display expenses, and persistent storage using JSON. Structured the project into modules (app, logic, storage, constants) to separate concerns.

Refactored UI layer:

- centralized all UI text in ui_text.py
- introduced language selection at startup (EN/LV)
- separated UI text from internal logic and data
- implemented category translation mapping (internal keys → localized labels)

Resolved JSON persistence issue:

removed global in-memory state
ensured fresh data load on each action (read-before-write pattern)

# 3. Discovered bugs and requested feature changes after testing
- amount should accept ',' and negative numbers (resolved)
- visual defect: at expenses list ui amount is close to category(resolved)
- use was getting incostitent suggestions for actions in case of invalid input. Created format_choice_error to properly manage this dynamically and not hardcoded as before.
- added confirmation before deleting
- made changes to alter inconsistencies in ui_text